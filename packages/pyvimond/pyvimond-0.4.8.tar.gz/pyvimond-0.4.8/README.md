# pyvimond

Tiny Python client library for various Vimond APIs. Currently it provides clients for:

* Vimond REST API
* Vimond Image Service

## Usage

The examples here can be found in the example files in the project root directory

### Vimond REST API

```python
from pyvimond.vimond_client import VimondClient

if __name__ == "__main__":
    # Create a client
    api_url = "https://vimond"
    user = "user"
    secret = "secret"
    vimond = VimondClient(api_url, user, secret)

    # Get an asset
    asset = vimond.get_asset(1334686)
    print(asset["uri"])

    # Get the asset's category
    category = vimond.get_category(asset["categoryId"])
    print(category["category"]["@uri"])
§
    # Get the metadata for the asset
    metadata = vimond.get_asset_metadata(1334686)
    print(metadata)
```

### Vimond Image Service

The client uses HTTP Basic authentication when interfacing with Vimond Image Service

```python
from pyvimond.vimond_image_service_client import VimondImageServiceClient

if __name__ == "__main__":
    # Create a client
    api_url = "https://image-service"
    username = "user"
    password = "secret"
    vimond_image_service = VimondImageServiceClient(api_url, username, password)

    # Create an image pack
    imagepack_id = vimond_image_service.create_image_pack()
    print(f"Created new imagepack with ID {imagepack_id}")

    # Update the "main" location with the image from a publicly accessible URL.
    # The function will return an ID consisting of the imagepack ID plus the current UNIX timestamp. This
    # can eventually be used to reference this version of the image (assuming it gets cached somewhere) even after
    # the image has been updated later on.
    public_url = "https://cdn.pixabay.com/photo/2020/12/03/12/35/sunset-5800386_960_720.jpg"
    timestamped_imagepack_id = vimond_image_service.send_image(imagepack_id, public_url, "main")

    # Get the URL to the timestamped version with location "main"
    url = vimond_image_service.create_image_url(timestamped_imagepack_id, location="main")
    print(url)

    # Get the URL to the untimestamped version and no location
    url_without_location = vimond_image_service.create_image_url(imagepack_id)
    print(url_without_location)
```

## Testing

```bash
python3 -m unittest discover
```

## Releasing

Before beginning, make sure you have the necessary tools installed:

```bash
pip install --user --upgrade setuptools wheel twine
```

To build a new distribution and publish it on PyPi:

1. Update the version number in `setup.py`
2. Run `make release`. When asked for credentials, use `__token__` as username and the output 
   of `vault -l pypi-pyvimond-api-token` as password.

More information: https://packaging.python.org/tutorials/packaging-projects/
