# MongoDB Data Faker

This project contains Python code to generate fake data for MongoDB. The code is organized into modules, and you can run individual files using the `-m` flag.

### Running a Single File

To run a specific file, use the `-m` flag followed by the module path. For example, to run the `fine.py` file located in the `models/fine` directory, use:
```sh
python -m models.fine.fine
```

### ENV
Make sure to set the `MONGO_URI` environment variable to the MongoDB connection string with valid username and password!


### Additional Information

- Ensure all dependencies are installed by running:
    ```sh
    pip install -r requirements.txt
    ```
### TODO
- [ ] Implement all models
- [ ] Implement all seeder functions

