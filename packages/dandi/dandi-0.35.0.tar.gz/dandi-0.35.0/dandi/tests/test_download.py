import json
import os
import os.path as op
import re
from shutil import rmtree

import pytest
import responses

from .skip import mark
from ..consts import DRAFT, dandiset_metadata_file
from ..dandiarchive import DandisetURL
from ..download import download, download_generator
from ..utils import list_paths


# both urls point to 000027 (lean test dataset), and both draft and "released"
# version have only a single file ATM
@mark.skipif_no_network
@pytest.mark.parametrize(
    "url",
    [  # Should go through API
        "https://dandiarchive.org/dandiset/000027/0.210831.2033",
        # Drafts do not go through API ATM, but that should not be visible to user
        "https://dandiarchive.org/dandiset/000027/draft",
    ],
)
def test_download_000027(url, tmpdir):
    ret = download(url, tmpdir)
    assert not ret  # we return nothing ATM, might want to "generate"
    dsdir = tmpdir / "000027"
    downloads = (x.relto(dsdir) for x in dsdir.visit())
    assert sorted(downloads) == [
        "dandiset.yaml",
        "sub-RAT123",
        op.join("sub-RAT123", "sub-RAT123.nwb"),
    ]
    # and checksum should be correct as well
    from ..support.digests import Digester

    assert (
        Digester(["md5"])(dsdir / "sub-RAT123" / "sub-RAT123.nwb")["md5"]
        == "33318fd510094e4304868b4a481d4a5a"
    )
    # redownload - since already exist there should be an exception
    with pytest.raises(FileExistsError):
        download(url, tmpdir)

    # TODO: somehow get that status report about what was downloaded and what not
    download(url, tmpdir, existing="skip")  # TODO: check that skipped
    download(url, tmpdir, existing="overwrite")  # TODO: check that redownloaded
    download(url, tmpdir, existing="refresh")  # TODO: check that skipped (the same)


@mark.skipif_no_network
@pytest.mark.parametrize(
    "url",
    [  # Should go through API
        "https://dandiarchive.org/dandiset/000027/0.210831.2033",
        # Drafts do not go through API ATM, but that should not be visible to user
        "https://dandiarchive.org/dandiset/000027/draft",
    ],
)
def test_download_000027_metadata_only(url, tmpdir):
    ret = download(url, tmpdir, get_assets=False)
    assert not ret  # we return nothing ATM, might want to "generate"
    dsdir = tmpdir / "000027"
    downloads = (x.relto(dsdir) for x in dsdir.visit())
    assert sorted(downloads) == ["dandiset.yaml"]


@mark.skipif_no_network
@pytest.mark.parametrize(
    "url",
    [  # Should go through API
        "https://dandiarchive.org/dandiset/000027/0.210831.2033",
        # Drafts do not go through API ATM, but that should not be visible to user
        "https://dandiarchive.org/dandiset/000027/draft",
    ],
)
def test_download_000027_assets_only(url, tmpdir):
    ret = download(url, tmpdir, get_metadata=False)
    assert not ret  # we return nothing ATM, might want to "generate"
    dsdir = tmpdir / "000027"
    downloads = (x.relto(dsdir) for x in dsdir.visit())
    assert sorted(downloads) == ["sub-RAT123", op.join("sub-RAT123", "sub-RAT123.nwb")]


@mark.skipif_no_network
@pytest.mark.parametrize("resizer", [lambda sz: 0, lambda sz: sz // 2, lambda sz: sz])
@pytest.mark.parametrize("version", ["0.210831.2033", DRAFT])
def test_download_000027_resume(tmp_path, resizer, version):
    from ..support.digests import Digester

    url = f"https://dandiarchive.org/dandiset/000027/{version}"
    digester = Digester()
    download(url, tmp_path, get_metadata=False)
    dsdir = tmp_path / "000027"
    nwb = dsdir / "sub-RAT123" / "sub-RAT123.nwb"
    digests = digester(str(nwb))
    dldir = nwb.with_name(nwb.name + ".dandidownload")
    dldir.mkdir()
    dlfile = dldir / "file"
    nwb.rename(dlfile)
    size = dlfile.stat().st_size
    os.truncate(dlfile, resizer(size))
    with (dldir / "checksum").open("w") as fp:
        json.dump(digests, fp)
    download(url, tmp_path, get_metadata=False)
    contents = [
        op.relpath(op.join(dirpath, entry), dsdir)
        for (dirpath, dirnames, filenames) in os.walk(dsdir)
        for entry in dirnames + filenames
    ]
    assert sorted(contents) == ["sub-RAT123", op.join("sub-RAT123", "sub-RAT123.nwb")]
    assert nwb.stat().st_size == size
    assert digester(str(nwb)) == digests


def test_download_newest_version(text_dandiset, tmp_path):
    dandiset = text_dandiset["dandiset"]
    dandiset_id = text_dandiset["dandiset_id"]
    download(dandiset.api_url, tmp_path)
    assert (tmp_path / dandiset_id / "file.txt").read_text() == "This is test text.\n"
    dandiset.wait_until_valid()
    dandiset.publish()
    (text_dandiset["dspath"] / "file.txt").write_text("This is different text.\n")
    text_dandiset["reupload"]()
    rmtree(tmp_path / dandiset_id)
    download(dandiset.api_url, tmp_path)
    assert (tmp_path / dandiset_id / "file.txt").read_text() == "This is test text.\n"


def test_download_folder(local_dandi_api, text_dandiset, tmp_path):
    dandiset_id = text_dandiset["dandiset_id"]
    download(
        f"dandi://{local_dandi_api['instance_id']}/{dandiset_id}/subdir2/", tmp_path
    )
    assert list_paths(tmp_path, dirs=True) == [
        tmp_path / "subdir2",
        tmp_path / "subdir2" / "banana.txt",
        tmp_path / "subdir2" / "coconut.txt",
    ]
    assert (tmp_path / "subdir2" / "banana.txt").read_text() == "Banana\n"
    assert (tmp_path / "subdir2" / "coconut.txt").read_text() == "Coconut\n"


def test_download_item(local_dandi_api, text_dandiset, tmp_path):
    dandiset_id = text_dandiset["dandiset_id"]
    download(
        f"dandi://{local_dandi_api['instance_id']}/{dandiset_id}/subdir2/coconut.txt",
        tmp_path,
    )
    assert list_paths(tmp_path, dirs=True) == [tmp_path / "coconut.txt"]
    assert (tmp_path / "coconut.txt").read_text() == "Coconut\n"


def test_download_asset_id(text_dandiset, tmp_path):
    asset = text_dandiset["dandiset"].get_asset_by_path("subdir2/coconut.txt")
    download(asset.download_url, tmp_path)
    assert list_paths(tmp_path, dirs=True) == [tmp_path / "coconut.txt"]
    assert (tmp_path / "coconut.txt").read_text() == "Coconut\n"


def test_download_asset_id_only(text_dandiset, tmp_path):
    asset = text_dandiset["dandiset"].get_asset_by_path("subdir2/coconut.txt")
    download(asset.base_download_url, tmp_path)
    assert list_paths(tmp_path, dirs=True) == [tmp_path / "coconut.txt"]
    assert (tmp_path / "coconut.txt").read_text() == "Coconut\n"


@pytest.mark.parametrize("confirm", [True, False])
def test_download_sync(confirm, local_dandi_api, mocker, text_dandiset, tmp_path):
    text_dandiset["dandiset"].get_asset_by_path("file.txt").delete()
    dspath = tmp_path / text_dandiset["dandiset_id"]
    os.rename(text_dandiset["dspath"], dspath)
    confirm_mock = mocker.patch(
        "dandi.download.abbrev_prompt", return_value="yes" if confirm else "no"
    )
    download(
        f"dandi://{local_dandi_api['instance_id']}/{text_dandiset['dandiset_id']}",
        tmp_path,
        existing="overwrite",
        sync=True,
    )
    confirm_mock.assert_called_with("Delete 1 local asset?", "yes", "no", "list")
    if confirm:
        assert not (dspath / "file.txt").exists()
    else:
        assert (dspath / "file.txt").exists()


def test_download_sync_folder(local_dandi_api, mocker, text_dandiset):
    text_dandiset["dandiset"].get_asset_by_path("file.txt").delete()
    text_dandiset["dandiset"].get_asset_by_path("subdir2/banana.txt").delete()
    confirm_mock = mocker.patch("dandi.download.abbrev_prompt", return_value="yes")
    download(
        f"dandi://{local_dandi_api['instance_id']}/{text_dandiset['dandiset_id']}/subdir2/",
        text_dandiset["dspath"],
        existing="overwrite",
        sync=True,
    )
    confirm_mock.assert_called_with("Delete 1 local asset?", "yes", "no", "list")
    assert (text_dandiset["dspath"] / "file.txt").exists()
    assert not (text_dandiset["dspath"] / "subdir2" / "banana.txt").exists()


def test_download_sync_list(capsys, local_dandi_api, mocker, text_dandiset, tmp_path):
    text_dandiset["dandiset"].get_asset_by_path("file.txt").delete()
    dspath = tmp_path / text_dandiset["dandiset_id"]
    os.rename(text_dandiset["dspath"], dspath)
    input_mock = mocker.patch("dandi.utils.input", side_effect=["list", "yes"])
    download(
        f"dandi://{local_dandi_api['instance_id']}/{text_dandiset['dandiset_id']}",
        tmp_path,
        existing="overwrite",
        sync=True,
    )
    assert not (dspath / "file.txt").exists()
    assert input_mock.call_args_list == [
        mocker.call("Delete 1 local asset? ([y]es/[n]o/[l]ist): "),
        mocker.call("Delete 1 local asset? ([y]es/[n]o/[l]ist): "),
    ]
    assert capsys.readouterr().out.splitlines()[-1] == str(dspath / "file.txt")


@responses.activate
def test_download_no_blobDateModified(text_dandiset, tmp_path):
    # Regression test for #806
    responses.add_passthru(re.compile("^http"))
    dandiset = text_dandiset["dandiset"]
    asset = dandiset.get_asset_by_path("file.txt")
    metadata = asset.get_raw_metadata()
    del metadata["blobDateModified"]
    responses.add(responses.GET, asset.api_url, json=metadata)
    download(dandiset.api_url, tmp_path)


@responses.activate
def test_download_metadata404(text_dandiset, tmp_path):
    responses.add_passthru(re.compile("^http"))
    asset = text_dandiset["dandiset"].get_asset_by_path("subdir1/apple.txt")
    responses.add(responses.GET, asset.api_url, status=404)
    statuses = list(
        download_generator(
            DandisetURL(
                api_url=text_dandiset["client"].api_url,
                dandiset_id=text_dandiset["dandiset"].identifier,
                version_id=text_dandiset["dandiset"].version_id,
            ),
            tmp_path,
        )
    )
    errors = [s for s in statuses if s.get("status") == "error"]
    assert errors == [
        {
            "path": "subdir1/apple.txt",
            "status": "error",
            "message": f"No such asset: {asset}",
        }
    ]
    assert list_paths(tmp_path, dirs=True) == [
        tmp_path / dandiset_metadata_file,
        tmp_path / "file.txt",
        tmp_path / "subdir2",
        tmp_path / "subdir2" / "banana.txt",
        tmp_path / "subdir2" / "coconut.txt",
    ]
