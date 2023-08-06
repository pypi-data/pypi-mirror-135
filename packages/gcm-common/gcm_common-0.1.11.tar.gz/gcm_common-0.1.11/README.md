# GCM Common Package

This is common library package for python/flask projects in GCM.

## Installation

```bash
pip install gcm-common
```

## What's in the package?

* Logging
* Custom Exception
* Response builder(Exception handling)
* Updater

## Usage

```python
import gcm_common
from flask import Flask

app = Flask(__name__)
# initialize error handling
gcm_common.json_error_handler(app=app)
# initialize logging
gcm_common.init_logger('path/to/conf_file')

# you could throw exception
raise gcm_common.MException(404, 'File Not Found')
# you could log information/error
gcm_common.error_log(os.path.basename(__file__), 'File Not Found!')
```

## Contributing

1. Make your changes in source code in gcm_common directory
2. Set new version in ./setup.py file
3. Export your new functions/classes in gcm_common/__init__.py
4. Delete archives in dist directory if there is any
5. Run following command to generate source distribution
    ```bash
    python setup.py sdist
    ```
6. Upload the new package to pip via twine
    1. install twine
        ```bash
        pip install twine
        ```
    2. Upload you package
       ```bash
       twine upload dist/*
       ```
    3. Fill in authentication form
        ```
       username: td.grapecity
       password: UBMongolia1234;
       ```