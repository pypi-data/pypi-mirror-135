# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at http://www.comet.ml
#  Copyright (C) 2015-2021 Comet ML INC
#  This file can not be copied and/or distributed
#  without the express permission of Comet ML Inc.
# *******************************************************

import io
import json
import os
import sys
import tempfile
import threading
from collections import namedtuple
from functools import partial
from logging import getLogger

import requests
import semantic_version
import six

from ._typing import Any, Dict, Iterable, List, Optional, Set, Tuple, Union
from .api import APIExperiment
from .config import Config
from .connection import RestApiClient, get_thread_session, write_stream_response_to_file
from .exceptions import (
    ArtifactAssetNotFound,
    ArtifactConflictingAssetLogicalPath,
    ArtifactDownloadException,
    ArtifactNotFinalException,
    ArtifactNotFound,
    CometRestApiException,
    GetArtifactException,
    LogArtifactException,
)
from .experiment import BaseExperiment
from .file_downloader import (
    FileDownloadManager,
    FileDownloadManagerMonitor,
    FileDownloadSizeMonitor,
)
from .file_uploader import (
    FileUpload,
    MemoryFileUpload,
    PreprocessedAsset,
    PreprocessedFileAsset,
    PreprocessedRemoteAsset,
    dispatch_user_file_upload,
    preprocess_asset_file,
    preprocess_asset_memory_file,
    preprocess_remote_asset,
)
from .file_utils import file_sha1sum, io_sha1sum
from .logging_messages import (
    ARTIFACT_ASSET_DOWNLOAD_FAILED,
    ARTIFACT_ASSET_UPLOAD_FAILED,
    ARTIFACT_DOWNLOAD_FILE_OVERWRITTEN,
    ARTIFACT_DOWNLOAD_FINISHED,
    ARTIFACT_DOWNLOAD_START_MESSAGE,
    ARTIFACT_UPLOAD_FINISHED,
    ARTIFACT_UPLOAD_STARTED,
    ARTIFACT_VERSION_CREATED_WITH_PREVIOUS,
    ARTIFACT_VERSION_CREATED_WITHOUT_PREVIOUS,
    LOG_ARTIFACT_IN_PROGESS_MESSAGE,
)
from .parallel_utils import makedirs_synchronized
from .summary import Summary
from .utils import (
    ImmutableDict,
    IterationProgressCallback,
    format_bytes,
    generate_guid,
    wait_for_done,
)
from .validation_utils import validate_metadata

LOGGER = getLogger(__name__)


def _parse_artifact_name(artifact_name):
    # type: (str) -> Tuple[Optional[str], str, Optional[str]]
    """Parse an artifact_name, potentially a fully-qualified name"""

    splitted = artifact_name.split("/")

    # First parse the workspace
    if len(splitted) == 1:
        workspace = None
        artifact_name_version = splitted[0]
    else:
        workspace = splitted[0]
        artifact_name_version = splitted[1]

    name_version_splitted = artifact_name_version.split(":", 1)

    if len(name_version_splitted) == 1:
        artifact_name = name_version_splitted[0]
        version_or_alias = None
    else:
        artifact_name = name_version_splitted[0]
        version_or_alias = name_version_splitted[1]

    return (workspace, artifact_name, version_or_alias)


def _log_artifact(artifact, experiment):
    # type: (Artifact, Any) -> LoggedArtifact
    artifact_id, artifact_version_id = _upsert_artifact(
        artifact, experiment.rest_api_client, experiment.id
    )

    success_prepared_request = _prepare_update_artifact_version_state(
        experiment.rest_api_client, artifact_version_id, experiment.id, "CLOSED"
    )
    timeout = experiment.config.get_int(None, "comet.timeout.http")
    verify_tls = experiment.config.get_bool(
        None, "comet.internal.check_tls_certificate"
    )

    logged_artifact = _get_artifact(
        experiment.rest_api_client,
        {"artifact_id": artifact_id, "artifact_version_id": artifact_version_id},
        experiment.id,
        experiment._summary,
        experiment.config,
    )

    if len(artifact._assets) == 0:
        LOGGER.warning(
            "Warning: Artifact %s created without adding any assets, was this the intent?",
            logged_artifact,
        )

        _call_post_prepared_request(
            success_prepared_request, timeout, verify_tls=verify_tls
        )
    else:
        failed_prepared_request = _prepare_update_artifact_version_state(
            experiment.rest_api_client, artifact_version_id, experiment.id, "ERROR"
        )

        _log_artifact_assets(
            artifact,
            experiment,
            artifact_version_id,
            logged_artifact.workspace,
            logged_artifact.name,
            str(logged_artifact.version),
            success_prepared_request,
            failed_prepared_request,
            timeout,
            verify_tls=verify_tls,
        )

        LOGGER.info(
            ARTIFACT_UPLOAD_STARTED,
            logged_artifact.workspace,
            logged_artifact.name,
            logged_artifact.version,
        )

    experiment._summary.increment_section("uploads", "artifacts")

    return logged_artifact


def _log_artifact_assets(
    artifact,  # type: Artifact
    experiment,  # type: BaseExperiment
    artifact_version_id,  # type: str
    logged_artifact_workspace,  # type: str
    logged_artifact_name,  # type: str
    logged_artifact_version,  # type: str
    success_prepared_request,  # type: Tuple[str, Dict[str, Any], Dict[str, Any]]
    failed_prepared_request,  # type: Tuple[str, Dict[str, Any], Dict[str, Any]]
    timeout,  # type: int
    verify_tls,  # type: bool
):
    # type: (...) -> None
    artifact_assets = artifact._assets.values()

    all_asset_ids = {artifact_asset.asset_id for artifact_asset in artifact_assets}

    lock = threading.Lock()

    # At the starts, it's the total numbers but then it's the remaining numbers
    num_assets = len(artifact_assets)
    total_size = sum(asset.size for asset in artifact_assets)

    LOGGER.info(
        "Scheduling the upload of %d assets for a size of %s, this can take some time",
        num_assets,
        format_bytes(total_size),
    )

    def progress_callback():
        LOGGER.info(
            LOG_ARTIFACT_IN_PROGESS_MESSAGE,
            num_assets,
            format_bytes(total_size),
        )

    frequency = 5

    success_log_message = ARTIFACT_UPLOAD_FINISHED
    success_log_message_args = (
        logged_artifact_workspace,
        logged_artifact_name,
        logged_artifact_version,
    )

    error_log_message = ARTIFACT_ASSET_UPLOAD_FAILED
    error_log_message_args = (
        logged_artifact_workspace,
        logged_artifact_name,
        logged_artifact_version,
    )

    for artifact_file in IterationProgressCallback(
        artifact_assets, progress_callback, frequency
    ):
        asset_id = artifact_file.asset_id

        # If the asset id is from a downloaded artifact version asset, generate a new ID here.
        # TODO: Need to find a way to not re-upload it
        if artifact_file.asset_id in artifact._downloaded_asset_ids:
            artifact_file = artifact_file._replace(asset_id=generate_guid())

        if isinstance(artifact_file, PreprocessedRemoteAsset):
            experiment._log_preprocessed_remote_asset(
                artifact_file,
                artifact_version_id=artifact_version_id,
                critical=True,
                on_asset_upload=partial(
                    _on_artifact_asset_upload,
                    lock,
                    all_asset_ids,
                    asset_id,
                    success_prepared_request,
                    timeout,
                    success_log_message,
                    success_log_message_args,
                    verify_tls,
                ),
                on_failed_asset_upload=partial(
                    _on_artifact_failed_asset_upload,
                    asset_id,
                    failed_prepared_request,
                    timeout,
                    error_log_message,
                    (asset_id,) + error_log_message_args,
                    verify_tls,
                ),
                return_url=False,
            )
        else:
            experiment._log_preprocessed_asset(
                artifact_file,
                artifact_version_id=artifact_version_id,
                critical=True,
                on_asset_upload=partial(
                    _on_artifact_asset_upload,
                    lock,
                    all_asset_ids,
                    asset_id,
                    success_prepared_request,
                    timeout,
                    success_log_message,
                    success_log_message_args,
                    verify_tls,
                ),
                on_failed_asset_upload=partial(
                    _on_artifact_failed_asset_upload,
                    asset_id,
                    failed_prepared_request,
                    timeout,
                    error_log_message,
                    (asset_id,) + error_log_message_args,
                    verify_tls,
                ),
                return_url=False,
            )
        num_assets -= 1
        total_size -= artifact_file.size


def _upsert_artifact(artifact, rest_api_client, experiment_key):
    # type: (Artifact, RestApiClient, str) -> Tuple[str, str]
    try:

        artifact_version = artifact.version
        if artifact_version is not None:
            artifact_version = str(artifact_version)

        response = rest_api_client.upsert_artifact(
            artifact_name=artifact.name,
            artifact_type=artifact.artifact_type,
            experiment_key=experiment_key,
            metadata=artifact.metadata,
            version=artifact_version,
            aliases=list(artifact.aliases),
            version_tags=list(artifact.version_tags),
        )
    except CometRestApiException as e:
        raise LogArtifactException(e.safe_msg, e.sdk_error_code)
    except requests.RequestException:
        raise LogArtifactException()

    result = response.json()

    artifact_id = result["artifactId"]
    artifact_version_id = result["artifactVersionId"]

    version = result["currentVersion"]
    _previous_version = result["previousVersion"]

    if _previous_version is None:
        LOGGER.info(ARTIFACT_VERSION_CREATED_WITHOUT_PREVIOUS, artifact.name, version)
    else:
        LOGGER.info(
            ARTIFACT_VERSION_CREATED_WITH_PREVIOUS,
            artifact.name,
            version,
            _previous_version,
        )

    return (artifact_id, artifact_version_id)


def _download_artifact_asset(
    url,  # type: str
    params,  # type: Dict[str, Any]
    headers,  # type: Dict[str, Any]
    timeout,  # type: int
    asset_id,  # type: str
    artifact_repr,  # type: str
    artifact_str,  # type: str
    asset_logical_path,  # type: str
    asset_path,  # type: str
    overwrite,  # type: str
    verify_tls,  # type: bool
    _monitor=None,  # type: Optional[FileDownloadSizeMonitor]
):
    # type: (...) -> None
    try:
        retry_session = get_thread_session(retry=True, verify_tls=verify_tls)

        response = retry_session.get(
            url=url,
            params=params,
            headers=headers,
            stream=True,
        )  # type: requests.Response

        if response.status_code != 200:
            response.close()
            raise CometRestApiException("GET", response)
    except Exception:
        raise ArtifactDownloadException(
            "Cannot download Asset %r for Artifact %s" % (asset_id, artifact_repr)
        )

    try:
        _write_artifact_asset_response_to_disk(
            artifact_str,
            asset_id,
            asset_logical_path,
            asset_path,
            overwrite,
            response,
            _monitor,
        )
    finally:
        try:
            response.close()
        except Exception:
            LOGGER.debug(
                "Error closing artifact asset download response", exc_info=True
            )
            pass


def _write_artifact_asset_response_to_disk(
    artifact_str,  # type: str
    asset_id,  # type: str
    asset_logical_path,  # type: str
    asset_path,  # type: str
    overwrite,  # type: str
    response,  # type: requests.Response
    monitor=None,  # type: Optional[FileDownloadSizeMonitor]
):
    # type: (...) -> None
    if os.path.isfile(asset_path):
        if overwrite == "OVERWRITE":
            LOGGER.warning(
                ARTIFACT_DOWNLOAD_FILE_OVERWRITTEN,
                asset_path,
                asset_logical_path,
                artifact_str,
            )
        elif overwrite == "PRESERVE":
            # TODO: Print LOG message if content is different when we have the SHA1 stored the
            # backend
            return
        else:
            # Download the file to a temporary file
            # TODO: Just compare the checksums
            try:
                existing_file_checksum = file_sha1sum(asset_path)
            except Exception:
                LOGGER.debug("Error computing sha1sum", exc_info=True)
                raise ArtifactDownloadException(
                    "Cannot read file %r to compare content, check logs for details"
                    % (asset_path)
                )

            try:
                with tempfile.NamedTemporaryFile() as f:
                    write_stream_response_to_file(response, f, None)

                    # Flush to be sure that everything is written
                    f.flush()
                    f.seek(0)

                    # Compute checksums
                    asset_checksum = io_sha1sum(f)

            except Exception:
                LOGGER.debug("Error write tmpfile to compute checksum", exc_info=True)
                raise ArtifactDownloadException(
                    "Cannot write Asset %r on disk path %r, check logs for details"
                    % (asset_id, asset_path)
                )

            if asset_checksum != existing_file_checksum:
                raise ArtifactDownloadException(
                    "Cannot write Asset %r on path %r, a file already exists"
                    % (
                        asset_id,
                        asset_path,
                    )
                )

            return None
    else:
        try:
            dirpart = os.path.dirname(asset_path)
            makedirs_synchronized(dirpart, exist_ok=True)
        except Exception:
            LOGGER.debug("Error creating directories", exc_info=True)
            raise ArtifactDownloadException(
                "Cannot write Asset %r on disk path %r, check logs for details"
                % (
                    asset_id,
                    asset_path,
                )
            )

    try:
        with io.open(asset_path, "wb") as f:
            write_stream_response_to_file(response, f, monitor)
    except Exception:
        LOGGER.debug("Error writing file on path", exc_info=True)
        raise ArtifactDownloadException(
            "Cannot write Asset %r on disk path %r, check logs for details"
            % (
                asset_id,
                asset_path,
            )
        )


def _on_artifact_asset_upload(
    lock,  # type: threading.Lock
    all_asset_ids,  # type: Set[str]
    asset_id,  # type: str
    prepared_request,  # type: Tuple[str, Dict[str, Any], Dict[str, Any]]
    timeout,  # type: int
    success_log_message,  # type: str
    success_log_message_args,  # type: Tuple
    verify_tls,  # type: bool
    response,  # type: Any
    *args,  # type: Any
    **kwargs  # type: Any
):
    # type: (...) -> None
    with lock:
        all_asset_ids.remove(asset_id)
        if len(all_asset_ids) == 0:
            try:
                _call_post_prepared_request(
                    prepared_request, timeout, verify_tls=verify_tls
                )
                LOGGER.info(success_log_message, *success_log_message_args)
            except Exception:
                LOGGER.error(
                    "Failed to mark the artifact version as closed", exc_info=True
                )


def _on_artifact_failed_asset_upload(
    asset_id,  # type: str
    prepared_request,  # type: Tuple[str, Dict[str, Any], Dict[str, Any]]
    timeout,  # type: int
    error_log_message,  # type: str
    error_log_message_args,  # type: Tuple
    verify_tls,  # type: bool
    response,  # type: Any
    *args,  # type: Any
    **kwargs  # type: Any
):
    # type: (...) -> None
    LOGGER.error(error_log_message, *error_log_message_args)

    try:
        _call_post_prepared_request(prepared_request, timeout, verify_tls=verify_tls)
    except Exception:
        LOGGER.error("Failed to mark the artifact version as error", exc_info=True)


def _call_post_prepared_request(prepared_request, timeout, verify_tls):
    # type: (Tuple[str, Dict[str, Any], Dict[str, Any]], int, bool) -> requests.Response
    session = get_thread_session(True, verify_tls=verify_tls)

    url, json_body, headers = prepared_request

    LOGGER.debug(
        "POST HTTP Call, url %r, json_body %r, timeout %r",
        url,
        json_body,
        timeout,
    )

    response = session.post(url, json=json_body, headers=headers, timeout=timeout)
    response.raise_for_status()
    return response


def _prepare_update_artifact_version_state(
    rest_api_client, artifact_version_id, experiment_key, state
):
    # type: (RestApiClient, str, str, str) -> Tuple[str, Dict[str, Any], Dict[str, Any]]
    # Extracted to ease the monkey-patching of Experiment.log_artifact
    return rest_api_client._prepare_update_artifact_version_state(
        artifact_version_id, experiment_key, state
    )


def _validate_overwrite_strategy(user_overwrite_strategy):
    # type: (Any) -> str

    if isinstance(user_overwrite_strategy, six.string_types):
        lower_user_overwrite_strategy = user_overwrite_strategy.lower()
    else:
        lower_user_overwrite_strategy = user_overwrite_strategy

    if (
        lower_user_overwrite_strategy is False
        or lower_user_overwrite_strategy == "fail"
    ):
        return "FAIL"

    elif lower_user_overwrite_strategy == "preserve":
        return "PRESERVE"

    elif (
        lower_user_overwrite_strategy is True
        or lower_user_overwrite_strategy == "overwrite"
    ):
        return "OVERWRITE"

    else:
        raise ValueError("Invalid user_overwrite value %r" % user_overwrite_strategy)


class Artifact(object):
    def __init__(
        self,
        name,  # type: str
        artifact_type,  # type: str
        version=None,  # type: Optional[str]
        aliases=None,  # type: Optional[Iterable[str]]
        metadata=None,  # type: Any
        version_tags=None,  # type: Optional[Iterable[str]]
    ):
        # type: (...) -> None
        """
        Comet Artifacts allow keeping track of assets beyond any particular experiment. You can keep
        track of Artifact versions, create many types of assets, manage them, and use them in any
        step in your ML pipelines---from training to production deployment.

        Artifacts live in a Comet Project, are identified by their name and version string number.

        Example how to log an artifact with an asset:

        ```python
        from comet_ml import Artifact, Experiment

        experiment = Experiment()
        artifact = Artifact("Artifact-Name", "Artifact-Type")
        artifact.add("local-file")

        experiment.log_artifact(artifact)
        experiment.end()
        ```

        Example how to get and download an artifact assets:

        ```python
        from comet_ml import Experiment

        experiment = Experiment()
        artifact = experiment.get_artifact("Artifact-Name", WORKSPACE, PROJECT_NAME)

        artifact.download("/data/input")
        ```

        The artifact is created on the frontend only when calling `Experiment.log_artifact`

        Args:
            name: The artifact name.
            artifact_type: The artifact-type, for example `dataset`.
            version: Optional. The version number to create. If not provided, a new version number
                will be created automatically.
            aliases: Optional. Iterable of String. Some aliases to attach to the future Artifact
                Version. The aliases list is converted into a set for de-duplication.
            metadata: Optional. Some additional data to attach to the future Artifact Version. Must
                be a JSON-encodable dict.
        """

        # Artifact fields
        self.artifact_type = artifact_type
        self.name = name

        # Upsert fields
        if version is None:
            self.version = None
        else:
            self.version = semantic_version.Version(version)

        self.version_tags = set()  # type: Set[str]
        if version_tags is not None:
            self.version_tags = set(version_tags)

        self.aliases = set()  # type: Set[str]
        if aliases is not None:
            self.aliases = set(aliases)

        self.metadata = validate_metadata(metadata, raise_on_invalid=True)

        self._assets = {}  # type: Dict[str, PreprocessedAsset]

        # The set of assets IDs that was already downloaded through LoggedArtifact.download
        self._downloaded_asset_ids = set()  # type: Set[str]

        self._download_local_path = None  # type: Optional[str]

    @classmethod
    def _from_logged_artifact(
        cls,
        name,  # type: str
        artifact_type,  # type: str
        assets,  # type: Dict[str, PreprocessedAsset]
        root_path,  # type: str
        asset_ids,  # type: Set[str]
    ):
        # type: (...) -> Artifact
        new_artifact = cls(name, artifact_type)
        new_artifact._assets = assets
        new_artifact._download_local_path = root_path
        new_artifact._downloaded_asset_ids = asset_ids

        return new_artifact

    def add(
        self,
        local_path_or_data,  # type: Any
        logical_path=None,  # type: Optional[str]
        overwrite=False,  # type: bool
        copy_to_tmp=True,  # type: bool # if local_path_or_data is a file pointer
        metadata=None,  # type: Any
    ):
        # type: (...) -> None
        """
        Add a local asset to the current pending artifact object.

        Args:
            local_path_or_data: String or File-like - either the file path of the file you want
                to log, or a file-like asset.
            logical_path: String - Optional. A custom file name to be displayed. If not
                provided the filename from the `local_path_or_data` argument will be used.
            overwrite: if True will overwrite all existing assets with the same name.
            copy_to_tmp: If `local_path_or_data` is a file-like object, then this flag determines
                if the file is first copied to a temporary file before upload. If
                `copy_to_tmp` is False, then it is sent directly to the cloud.
            metadata: Optional. Some additional data to attach to the the audio asset. Must be a
                JSON-encodable dict.
        """
        if local_path_or_data is None:
            raise TypeError("local_path_or_data cannot be None")

        dispatched = dispatch_user_file_upload(local_path_or_data)
        asset_id = generate_guid()

        if not isinstance(dispatched, (FileUpload, MemoryFileUpload)):
            raise ValueError(
                "Invalid file_data %r, must either be a valid file-path or an IO object"
                % local_path_or_data
            )
        elif isinstance(dispatched, FileUpload):
            preprocessed = preprocess_asset_file(
                dispatched=dispatched,
                upload_type="asset",
                file_name=logical_path,
                metadata=metadata,
                overwrite=overwrite,
                asset_id=asset_id,
                copy_to_tmp=copy_to_tmp,
            )
        else:
            preprocessed = preprocess_asset_memory_file(
                dispatched=dispatched,
                upload_type="asset",
                file_name=logical_path,
                metadata=metadata,
                overwrite=overwrite,
                copy_to_tmp=copy_to_tmp,
            )

        self._add_preprocessed(preprocessed)

    def add_remote(
        self,
        uri,  # type: Any
        logical_path=None,  # type: Optional[str]
        overwrite=False,  # type: bool
        asset_type="asset",  # type: str
        metadata=None,  # type: Any
    ):
        # type: (...) -> None
        """
        Add a remote asset to the current pending artifact object. A Remote Asset is an asset but
        its content is not uploaded and stored on Comet. Rather a link for its location is stored so
        you can identify and distinguish between two experiment using different version of a dataset
        stored somewhere else.

        Args:
            uri: String - the remote asset location, there is no imposed format and it could be a
                private link.
            logical_path: String, Optional. The "name" of the remote asset, could be a dataset
                name, a model file name.
            overwrite: if True will overwrite all existing assets with the same name.
            metadata: Some additional data to attach to the the remote asset.
                Must be a JSON-encodable dict.
        """
        preprocessed = preprocess_remote_asset(
            uri,
            logical_path,
            overwrite,
            asset_type,
            metadata=metadata,
        )

        self._add_preprocessed(preprocessed)

    def _preprocessed_user_input(self, preprocessed):
        # type: (PreprocessedAsset) -> Any
        if isinstance(preprocessed, PreprocessedRemoteAsset):
            return preprocessed.remote_uri
        else:
            return preprocessed.local_path_or_data

    def _add_preprocessed(self, preprocessed):
        # type: (PreprocessedAsset) -> None
        preprocessed_logical_path = preprocessed.logical_path

        if preprocessed_logical_path in self._assets:
            # Allow the overriding of an asset inherited from a downloaded version
            if (
                self._assets[preprocessed_logical_path].asset_id
                in self._downloaded_asset_ids
            ):
                self._downloaded_asset_ids.remove(
                    self._assets[preprocessed_logical_path].asset_id
                )
                self._assets[preprocessed_logical_path] = preprocessed
            else:
                raise ArtifactConflictingAssetLogicalPath(
                    self._preprocessed_user_input(
                        self._assets[preprocessed_logical_path]
                    ),
                    self._preprocessed_user_input(preprocessed),
                    preprocessed_logical_path,
                )
        else:
            self._assets[preprocessed_logical_path] = preprocessed

    def __str__(self):
        return "%s(%r, artifact_type=%r)" % (
            self.__class__.__name__,
            self.name,
            self.artifact_type,
        )

    def __repr__(self):
        return (
            "%s(name=%r, artifact_type=%r, version=%r, aliases=%r, version_tags=%s)"
            % (
                self.__class__.__name__,
                self.name,
                self.artifact_type,
                self.version,
                self.aliases,
                self.version_tags,
            )
        )

    @property
    def assets(self):
        """
        The list of `ArtifactAssets` that have been logged with this `Artifact`.
        """
        artifact_version_assets = []

        for asset in self._assets.values():

            if isinstance(asset, PreprocessedRemoteAsset):
                artifact_version_assets.append(
                    ArtifactAsset(
                        True,
                        asset.logical_path,
                        0,  # Semantically remote files have a 0 size but we are still counting the size for upload progress
                        asset.remote_uri,
                        asset.metadata,
                        asset.upload_type,
                        None,
                    )
                )
            else:
                artifact_version_assets.append(
                    ArtifactAsset(
                        False,
                        asset.logical_path,
                        asset.size,
                        None,
                        asset.metadata,
                        None,
                        asset.local_path_or_data,
                    )
                )

        return artifact_version_assets

    @property
    def download_local_path(self):
        # type: () -> Optional[str]
        """If the Artifact object was returned by `LoggedArtifact.download`, returns the root path
        where the assets has been downloaded. Else, returns None.
        """
        return self._download_local_path


def _get_artifact(rest_api_client, get_artifact_params, experiment_id, summary, config):
    # type: (RestApiClient, Dict[str, Optional[str]], str, Summary, Config) -> LoggedArtifact

    try:
        result = rest_api_client.get_artifact_version_details(**get_artifact_params)
    except CometRestApiException as e:
        if e.sdk_error_code == 624523:
            raise ArtifactNotFound("Artifact not found with %r" % (get_artifact_params))
        if e.sdk_error_code == 90403 or e.sdk_error_code == 90402:
            raise ArtifactNotFinalException(
                "Artifact %r is not in a finalized state and cannot be accessed"
                % (get_artifact_params)
            )

        raise
    except Exception:
        raise GetArtifactException(
            "Get artifact failed with an error, check the logs for details"
        )

    artifact_name = result["artifact"]["artifactName"]
    artifact_version = result["artifactVersion"]
    artifact_metadata = result["metadata"]
    if artifact_metadata:
        try:
            artifact_metadata = json.loads(artifact_metadata)
        except Exception:
            LOGGER.warning(
                "Couldn't decode metadata for artifact %r:%r"
                % (artifact_name, artifact_version)
            )
            artifact_metadata = None

    return LoggedArtifact(
        aliases=result["alias"],
        artifact_id=result["artifact"]["artifactId"],
        artifact_name=artifact_name,
        artifact_tags=result["artifact"]["tags"],
        artifact_type=result["artifact"]["artifactType"],
        artifact_version_id=result["artifactVersionId"],
        config=config,
        experiment_key=experiment_id,  # TODO: Remove ME
        metadata=artifact_metadata,
        rest_api_client=rest_api_client,
        size=result["sizeInBytes"],
        source_experiment_key=result["experimentKey"],
        summary=summary,
        version_tags=result["tags"],
        version=artifact_version,
        workspace=result["artifact"]["workspaceName"],
    )


class LoggedArtifact(object):
    def __init__(
        self,
        artifact_name,
        artifact_type,
        artifact_id,
        artifact_version_id,
        workspace,
        rest_api_client,  # type: RestApiClient
        experiment_key,
        version,
        aliases,
        artifact_tags,
        version_tags,
        size,
        metadata,
        source_experiment_key,  # type: str
        summary,
        config,  # type: Config
    ):
        # type: (...) -> None
        """
        You shouldn't try to create this object by hand, please use
        [Experiment.get_artifact()](/docs/python-sdk/Experiment/#experimentget_artifact) instead to
        retrieve an artifact.
        """
        # Artifact fields
        self._artifact_type = artifact_type
        self._name = artifact_name
        self._artifact_id = artifact_id
        self._artifact_version_id = artifact_version_id

        self._version = semantic_version.Version(version)
        self._aliases = frozenset(aliases)
        self._rest_api_client = rest_api_client
        self._workspace = workspace
        self._artifact_tags = frozenset(artifact_tags)
        self._version_tags = frozenset(version_tags)
        self._size = size
        self._source_experiment_key = source_experiment_key
        self._experiment_key = experiment_key  # TODO: Remove ME
        self._summary = summary
        self._config = config

        if metadata is not None:
            self._metadata = ImmutableDict(metadata)
        else:
            self._metadata = ImmutableDict()

    def _raw_assets(self):
        """Returns the artifact version ID assets"""
        return self._rest_api_client.get_artifact_files(
            workspace=self._workspace,
            name=self._name,
            version=str(self.version),
        )["files"]

    def _to_logged_artifact(self, raw_artifact_asset):
        # type: (Dict[str, Any]) -> LoggedArtifactAsset

        if "remote" in raw_artifact_asset:
            remote = raw_artifact_asset["remote"]
        else:
            remote = (
                raw_artifact_asset["link"] is not None
            )  # TODO: Remove me after October 1st

        return LoggedArtifactAsset(
            remote,
            raw_artifact_asset["fileName"],
            raw_artifact_asset["fileSize"],
            raw_artifact_asset["link"],
            raw_artifact_asset["metadata"],
            raw_artifact_asset["type"],
            raw_artifact_asset["assetId"],
            self._artifact_version_id,
            self._artifact_id,
            self._source_experiment_key,
            verify_tls=self._config.get_bool(
                None, "comet.internal.check_tls_certificate"
            ),
            rest_api_client=self._rest_api_client,
            download_timeout=self._config.get_int(None, "comet.timeout.file_download"),
            logged_artifact_repr=self.__repr__(),
            logged_artifact_str=self.__str__(),
            experiment_key=self._experiment_key,
        )

    @property
    def assets(self):
        # type: () -> List[LoggedArtifactAsset]
        """
        The list of `LoggedArtifactAsset` that have been logged with this `LoggedArtifact`.
        """
        artifact_version_assets = []

        for asset in self._raw_assets():
            artifact_version_assets.append(self._to_logged_artifact(asset))

        return artifact_version_assets

    @property
    def remote_assets(self):
        # type: () -> List[LoggedArtifactAsset]
        """
        The list of remote `LoggedArtifactAsset` that have been logged with this `LoggedArtifact`.
        """
        artifact_version_assets = []

        for asset in self._raw_assets():
            if "remote" in asset:
                remote = asset["remote"]
            else:
                remote = asset["link"] is not None  # TODO: Remove me after October 1st

            if not remote:
                continue

            artifact_version_assets.append(self._to_logged_artifact(asset))

        return artifact_version_assets

    def get_asset(self, asset_logical_path):
        # type: (str) -> LoggedArtifactAsset
        """
        Returns the LoggedArtifactAsset object matching the given asset_logical_path or raises an Exception
        """
        for asset in self._raw_assets():
            if asset["fileName"] == asset_logical_path:
                return self._to_logged_artifact(asset)

        raise ArtifactAssetNotFound(asset_logical_path, self)

    def download(
        self,
        path=None,
        overwrite_strategy=False,
    ):
        # type: (Optional[str], Union[bool, str]) -> Artifact
        """
        Download the current Artifact Version assets to a given directory (or the local directory by
        default). This downloads only non-remote assets. You can access remote assets link with the
        `artifact.assets` property.

        Args:
            path: String, Optional. Where to download artifact version assets. If not provided,
                a temporay path will be used, the root path can be accessed through the Artifact object
                which is returned by download under the `.download_local_path` attribute.
            overwrite_strategy: String or Boolean. One of the three possible strategies to handle
                conflict when trying to download an artifact version asset to a path with an existing
                file. See below for allowed values. Default is False or "FAIL".

        Overwrite strategy allowed values:

            * False or "FAIL": If a file already exists and its content is different, raise the
            `comet_ml.exceptions.ArtifactDownloadException`.
            * "PRESERVE": If a file already exists and its content is different, show a WARNING but
            preserve the existing content.
            * True or "OVERWRITE": If a file already exists and its content is different, replace it
            by the asset version asset.

        Returns: Artifact object
        """

        if path is None:
            root_path = tempfile.mkdtemp()
        else:
            root_path = path

        overwrite_strategy = _validate_overwrite_strategy(overwrite_strategy)

        new_artifact_assets = {}  # type: Dict[str, PreprocessedAsset]
        new_artifact_asset_ids = set()

        try:
            raw_assets = self._raw_assets()
        except Exception:
            raise ArtifactDownloadException(
                "Cannot get asset list for Artifact %r" % self
            )

        worker_cpu_ratio = self._config.get_int(
            None, "comet.internal.file_upload_worker_ratio"
        )
        download_manager = FileDownloadManager(worker_cpu_ratio=worker_cpu_ratio)

        file_download_timeout = self._config.get_int(
            None, "comet.timeout.file_download"
        )
        verify_tls = self._config.get_bool(None, "comet.internal.check_tls_certificate")

        results = []

        self_repr = repr(self)
        self_str = str(self)

        for asset in raw_assets:
            asset_metadata = asset["metadata"]
            if asset_metadata is not None:
                asset_metadata = json.loads(asset["metadata"])

            if "remote" in asset:
                asset_remote = asset["remote"]
            else:
                asset_remote = (
                    asset["link"] is not None
                )  # TODO: Remove me after October 1st

            if asset_remote is True:
                # We don't download remote assets
                asset_filename = asset["fileName"]
                asset_id = asset["assetId"]

                new_artifact_assets[asset_filename] = PreprocessedRemoteAsset(
                    remote_uri=asset["link"],
                    overwrite=False,
                    upload_type=asset["type"],
                    metadata=asset_metadata,
                    step=None,
                    asset_id=asset_id,
                    logical_path=asset_filename,
                    size=len(asset["link"]),
                )
                new_artifact_asset_ids.add(asset_id)

                self._summary.increment_section("downloads", "artifact assets")
            else:
                asset_filename = asset["fileName"]
                asset_path = os.path.join(root_path, asset_filename)
                asset_id = asset["assetId"]
                prepared_request = (
                    self._rest_api_client._prepare_experiment_asset_request(
                        asset_id, self._experiment_key, asset["artifactVersionId"]
                    )
                )
                url, params, headers = prepared_request

                # register asset to be downloaded
                result = download_manager.download_file_async(
                    _download_artifact_asset,
                    url=url,
                    params=params,
                    headers=headers,
                    timeout=file_download_timeout,
                    verify_tls=verify_tls,
                    asset_id=asset_id,
                    artifact_repr=self_repr,
                    artifact_str=self_str,
                    asset_logical_path=asset_filename,
                    asset_path=asset_path,
                    overwrite=overwrite_strategy,
                    estimated_size=asset["fileSize"],
                )

                results.append(
                    (result, asset_filename, asset_path, asset_metadata, asset_id)
                )

        # Forbid new usage
        download_manager.close()

        # Wait for download manager to complete registered file downloads
        if not download_manager.all_done():
            monitor = FileDownloadManagerMonitor(download_manager)

            LOGGER.info(
                ARTIFACT_DOWNLOAD_START_MESSAGE,
                self._workspace,
                self._name,
                self._version,
            )

            wait_for_done(
                check_function=monitor.all_done,
                timeout=self._config.get_int(None, "comet.timeout.artifact_download"),
                progress_callback=monitor.log_remaining_downloads,
                sleep_time=15,
            )

        # iterate over download results and create file assets descriptors
        try:
            for (
                result,
                result_asset_filename,
                result_asset_path,
                result_asset_metadata,
                asset_id,
            ) in results:
                try:
                    result.get(file_download_timeout)

                    new_asset_size = os.path.getsize(result_asset_path)
                except Exception:
                    # display failed message
                    LOGGER.error(
                        ARTIFACT_ASSET_DOWNLOAD_FAILED,
                        result_asset_filename,
                        self._workspace,
                        self._name,
                        self._version,
                        exc_info=True,
                    )

                    raise ArtifactDownloadException(
                        "Cannot download Asset %s for Artifact %s"
                        % (result_asset_filename, self_repr)
                    )

                self._summary.increment_section(
                    "downloads",
                    "artifact assets",
                    size=new_asset_size,
                )

                new_artifact_assets[result_asset_filename] = PreprocessedFileAsset(
                    local_path_or_data=result_asset_path,
                    upload_type="asset",  # TODO: FIXME
                    logical_path=result_asset_filename,
                    metadata=result_asset_metadata,
                    overwrite=False,
                    step=None,
                    asset_id=asset_id,
                    grouping_name=None,  # TODO: FIXME?
                    extension=None,  # TODO: FIXME?
                    size=new_asset_size,
                    copy_to_tmp=False,
                )

                new_artifact_asset_ids.add(asset_id)

            # display success message
            LOGGER.info(
                ARTIFACT_DOWNLOAD_FINISHED, self._workspace, self._name, self._version
            )
        finally:
            download_manager.join()

        return Artifact._from_logged_artifact(
            self._name,
            self._artifact_type,
            new_artifact_assets,
            root_path,
            new_artifact_asset_ids,
        )

    def get_source_experiment(
        self,
        api_key=None,
        cache=True,
    ):
        # type: (Optional[str], bool) -> APIExperiment
        """
        Returns an APIExperiment object pointing to the experiment that created this artifact version, assumes that the API key is set else-where.
        """
        return APIExperiment(
            api_key=api_key,
            cache=cache,
            previous_experiment=self._source_experiment_key,
        )

    # Public properties
    @property
    def name(self):
        """
        The logged artifact name.
        """
        return self._name

    @property
    def artifact_type(self):
        """
        The logged artifact type.
        """
        return self._artifact_type

    @property
    def version(self):
        """
        The logged artifact version, as a SemanticVersion. See
        https://python-semanticversion.readthedocs.io/en/latest/reference.html#semantic_version.Version
        for reference
        """
        return self._version

    @property
    def workspace(self):
        """
        The logged artifact workspace name.
        """
        return self._workspace

    @property
    def aliases(self):
        """
        The set of logged artifact aliases.
        """
        return self._aliases

    @property
    def metadata(self):
        """
        The logged artifact metadata.
        """
        return self._metadata

    @property
    def version_tags(self):
        """
        The set of logged artifact version tags.
        """
        return self._version_tags

    @property
    def artifact_tags(self):
        """
        The set of logged artifact tags.
        """
        return self._artifact_tags

    @property
    def size(self):
        """
        The total size of logged artifact version; it is the sum of all the artifact version assets.
        """
        return self._size

    @property
    def source_experiment_key(self):
        """
        The experiment key of the experiment that created this LoggedArtifact.
        """
        return self._source_experiment_key

    def __str__(self):
        return "<%s '%s/%s:%s'>" % (
            self.__class__.__name__,
            self._workspace,
            self._name,
            self._version,
        )

    def __repr__(self):
        return self.__class__.__name__ + "(artifact_name=%r, artifact_type=%r, workspace=%r, version=%r, aliases=%r, artifact_tags=%r, version_tags=%r, size=%r, source_experiment_key=%r)" % (
            self._name,
            self._artifact_type,
            self._workspace,
            self._version,
            self._aliases,
            self._artifact_tags,
            self._version_tags,
            self._size,
            self._source_experiment_key,
        )


ArtifactAsset = namedtuple(
    "ArtifactAsset",
    [
        "remote",
        "logical_path",
        "size",
        "link",
        "metadata",
        "asset_type",
        "local_path_or_data",
    ],
)


class LoggedArtifactAsset(object):

    """
    LoggedArtifactAsset(remote, logical_path, size, link, metadata, asset_type, id,
    artifact_version_id, artifact_id, source_experiment_key): represent assets logged to an Artifact
    """

    __slots__ = (
        "_remote",
        "_logical_path",
        "_size",
        "_link",
        "_metadata",
        "_asset_type",
        "_id",
        "_artifact_version_id",
        "_artifact_id",
        "_source_experiment_key",
        "_rest_api_client",
        "_download_timeout",
        "_logged_artifact_repr",
        "_logged_artifact_str",
        "_experiment_key",
        "_verify_tls",
    )

    def __init__(
        self,
        remote,
        logical_path,
        size,
        link,
        metadata,
        asset_type,
        id,
        artifact_version_id,
        artifact_id,
        source_experiment_key,
        verify_tls,  # type: bool
        rest_api_client=None,
        download_timeout=None,
        logged_artifact_repr=None,
        logged_artifact_str=None,
        experiment_key=None,
    ):
        # type: (...) -> None
        self._remote = remote
        self._logical_path = logical_path
        self._size = size
        self._link = link
        self._metadata = metadata
        self._asset_type = asset_type
        self._id = id
        self._artifact_version_id = artifact_version_id
        self._artifact_id = artifact_id
        self._source_experiment_key = source_experiment_key

        self._rest_api_client = rest_api_client
        self._download_timeout = download_timeout
        self._verify_tls = verify_tls
        self._logged_artifact_repr = logged_artifact_repr
        self._logged_artifact_str = logged_artifact_str
        self._experiment_key = experiment_key

    @property
    def remote(self):
        "Is the asset a remote asset or not, boolean"
        return self._remote

    @property
    def logical_path(self):
        "Asset relative logical_path, str or None"
        return self._logical_path

    @property
    def size(self):
        "Asset size if the asset is a non-remote asset, int"
        return self._size

    @property
    def link(self):
        "Asset remote link if the asset is remote, str or None"
        return self._link

    @property
    def metadata(self):
        "Asset metadata, dict"
        return self._metadata

    @property
    def asset_type(self):
        "Asset type, str"
        return self._asset_type

    @property
    def id(self):
        "Asset unique id, str"
        return self._id

    @property
    def artifact_version_id(self):
        "Artifact version id, str"
        return self._artifact_version_id

    @property
    def artifact_id(self):
        "Artifact id, str"
        return self._artifact_id

    @property
    def source_experiment_key(self):
        "The experiment key of the experiment that logged this asset, str"
        return self._source_experiment_key

    def __repr__(self):
        return "%s(remote=%r, logical_path=%r, size=%r, link=%r, metadata=%r, asset_type=%r, id=%r, artifact_version_id=%r, artifact_id=%r, source_experiment_key=%r)" % (
            self.__class__.__name__,
            self._remote,
            self._logical_path,
            self._size,
            self._link,
            self._metadata,
            self._asset_type,
            self._id,
            self._artifact_version_id,
            self._artifact_id,
            self._source_experiment_key,
        )

    def __eq__(self, other):
        return (
            self._remote == other._remote
            and self._logical_path == other._logical_path
            and self._size == other._size
            and self._link == other._link
            and self._metadata == other._metadata
            and self._asset_type == other._asset_type
            and self._id == other._id
            and self._artifact_version_id == other._artifact_version_id
            and self._artifact_id == other._artifact_id
            and self._source_experiment_key == other._source_experiment_key
        )

    def __lt__(self, other):
        return self._logical_path < other._logical_path

    def download(
        self,
        local_path=None,  # if None, downloads to a tmp path
        logical_path=None,
        overwrite_strategy=False,
    ):
        """
        Download the asset to a given full path or directory

        Returns: ArtifactAsset object

        Args:
          local_path: the root folder to which to download.
            if None, will download to a tmp path
            if str, will be either a root local path or a full local path

          logical_path: the path relative to the root local_path to use
            if None and local_path==None then no relative path is used,
              file would just be a tmp path on local disk
            if None and local_path!=None then the local_path will be treated
              as a root path, and the asset's logical_path will be appended
              to the root path to form a full local path
            if "" or False then local_path will be used as a full path
              (local_path can also be None)

            overwrite_strategy: can be False, "FAIL", "PRESERVE" or "OVERWRITE"
              and follows the same semantics for overwrite strategy as artifact.download()
        """
        if local_path is None:
            root_path = tempfile.mkdtemp()
        else:
            root_path = local_path

        if logical_path is None:
            asset_filename = self._logical_path
        else:
            asset_filename = logical_path

        result_asset_path = os.path.join(root_path, asset_filename)

        prepared_request = self._rest_api_client._prepare_experiment_asset_request(
            self._id, self._experiment_key, self._artifact_version_id
        )
        url, params, headers = prepared_request

        _download_artifact_asset(
            url,
            params,
            headers,
            self._download_timeout,
            self._id,
            self._logged_artifact_repr,
            self._logged_artifact_str,
            asset_filename,
            result_asset_path,
            _validate_overwrite_strategy(overwrite_strategy),
            verify_tls=self._verify_tls,
        )

        return ArtifactAsset(
            remote=False,
            logical_path=self._logical_path,
            size=self._size,
            link=None,
            metadata=self._metadata,
            asset_type=self._asset_type,
            local_path_or_data=result_asset_path,
        )


# NamedTuple docstring can only be update starting with Python 3.5
if sys.version_info >= (3, 5):
    ArtifactAsset.__doc__ += ": represent local and remote assets added to an Artifact object but not yet uploaded"
    ArtifactAsset.remote.__doc__ = "Is the asset a remote asset or not, boolean"
    ArtifactAsset.logical_path.__doc__ = "Asset relative logical_path, str or None"
    ArtifactAsset.size.__doc__ = "Asset size if the asset is a non-remote asset, int"
    ArtifactAsset.link.__doc__ = "Asset remote link if the asset is remote, str or None"
    ArtifactAsset.metadata.__doc__ = "Asset metadata, dict"
    ArtifactAsset.asset_type.__doc__ = "Asset type if the asset is remote, str or None"
    ArtifactAsset.local_path_or_data.__doc__ = "Asset local path or in-memory file if the asset is non-remote, str, memory-file or None"
