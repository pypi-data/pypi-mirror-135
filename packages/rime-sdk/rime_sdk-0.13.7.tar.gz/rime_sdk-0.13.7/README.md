# RIME SDK

The RIME SDK provides an interface to RIME backend services for starting and viewing the progress of RIME stress test jobs.
There are four objects available in the `rime_sdk` package:
* RIMEClient
* RIMEStressTestJob
* RIMEProject
* CustomImage

To use these objects, import them from the package like so:
```Python
from rime_sdk import RIMEClient, RIMEStressTestJob, RIMEProject, CustomImage
```

## RIMEClient

The `RIMEClient` provides an interface to RIME's backend services for creating projects, starting stress test jobs, and querying the backend for current stress test jobs.
To initialize the RIMEClient, provide the address of your RIME instance.
```Python
rime_client = RIMEClient("my_vpc.rime.com", "api-key")
```

### `start_stress_test()`

This allows you to start an AI Stress Testing job on the RIME backend.

**Arguments:**

* `test_run_config: dict`

  Specifies paths to the model and dataset to be used in stress testing.
* `project_id: Optional[str] = None`

  Specify the project to file the stress test result under.
  If omitted, the stress test result will be stored in the default project.

* `rime_managed_image: Optional[str] = None`

  Specify the name of the RIME Managed Image to run the stress test on.
  Managed Images are the preferred method of running RIME on an image with custom Pip requirements.
  See the documentation for `create_managed_image()` and `list_managed_images()` for further information.

* `custom_image: Optional[CustomImage] = None`

  Specify a custom Docker image to run the stress test job on.
  This image could include custom libraries that your model depends on.
  If no custom image is provided, the backend will use the default image specified by the cluster configuration.

**Return Value:**

A `RIMEStressTestJob` object that provides an interface for monitoring the job in the backend.

**Example:**

```Python
# This example will likely not work for you because it requires permissions to a specific S3 bucket.
# This demonstrates how you might specify such a configuration.
config = {
  "run_name": "Titanic",
  "data_info": {
    "label_col": "Survived",
    "ref_path": "s3://rime-datasets/titanic/titanic_example.csv", "eval_path": "s3://rime-datasets/titanic/titanic_example.csv"
  },
  "model_info": {
    "path": "s3://rime-models/titanic_s3_test/titanic_example_model.py"
  }
}
# Run the job using the specified config and the default Docker image in the RIME backend.
# Store the results under project ID "foo"
# Use the RIME Managed Image "tensorflow115".
# This assumes you have already created the Managed Image and waited for it to be ready.
job = rime_client.start_stress_test_job(test_run_config=config, project_id="foo", rime_managed_image="tensorflow115")
```

### `create_managed_image()`

This method allow you to create new managed Docker images to run RIME on.
These managed Docker images are managed by the RIME backend and will automatically be upgraded when you update your version of RIME.
Images take a few minutes to be built.
This method returns an object that can be used to track the progress of the image building job.
The new custom image is only available for use in a stress test once it has status `READY`.

**Arguments**

* `name: str`

  The name of the new managed image.
  This acts as the unique identifier of the managed image.
  The call will fail if an image with the specified name already exists.

* `requirements: List[ManagedImage.PipRequirement]`

  List of additional pip requirements to be installed on the managed image.
  A `ManagedImage.PipRequirement` can be created with the helper method `RIMEClient.pip_requirement(name: str, version_specifier: Optional[str] = None)`.
  The first argument is the name of the library (e.g. `"tensorflow"` or `"xgboost"`) and the second argument is a valid pip
  [version specifier](https://www.python.org/dev/peps/pep-0440/#version-specifiers) (e.g. `">=0.1.2"` or `"==1.0.2"`).

**Return Value**

A `RIMEImageBuilder` object that provides an interface for monitoring the job in the backend.

**Example**

```python
requirements = [
   # Fix the version of `xgboost` to `1.0.2`.
   rime_client.pip_requirement("xgboost", "==1.0.2"),
   # We do not care about the installed version of `tensorflow`.
   rime_client.pip_requirement("tensorflow")
 ]

# Start a new image building job 
builder_job = rime_client.create_managed_image("xgboost102_tensorflow", requirements)
# Wait until the job has finished and print out status information.
# Once this prints out the `READY` status, your image is available for use in stress tests.
builder_job.get_status(verbose=True, wait_until_finish=True)
```

### `list_managed_images()`

This method allows you to query the backend for managed Docker images.
This is where the true power of the managed images feature lies.
You can search for images with specific pip libraries installed so that you do not have to create a new managed image every time you need to run a stress test.

**Arguments**

* `pip_library_filters: Optional[List[ListImagesRequest.PipLibraryFilter]] = None`

  A list of filters used to query the managed images stored in the backend.
  Query results will match the intersection of the filters.
  You may construct `ListImagesRequest.PipLibraryFilter` objects using the `RIMEClient.pip_library_filter(name: str, fixed_version: Optional[str] = None)` helper method.


* `page_token: str = ""`

  Page token used for paginating the API results.
  To get access to the next page of results, use the second value in the tuple returned by the previous call.

* `page_size: int = 100`

  Number of results to output.
  Default is 100 managed images to be returned.

**Return Value**

A `Tuple[List[Dict], str]` object.
The first value in the tuple is a list of dictionary representations of Managed Images.
The second value in the tuple is the next page token.

**Example**

```python
# Filter for an image with catboost1.0.3 and tensorflow installed.
filters = [
  rime_client.pip_library_filter("catboost", "1.0.3"),
  rime_client.pip_library_filter("tensorflow"),
]

# Query for the images.
images, next_page_token = rime_client.list_managed_images(pip_library_filters=filters)

# List comprehension to get all the names of the images.
names = [x["name"] for x in images]
```

### `create_project()`

Projects allow you to organize stress test runs as you see fit.
A natural way to organize stress test runs is to create a project for each specific ML task, such as predicting whether a transaction is fradulent.

**Arguments:**

* `name: str`

  The name of the project.
  You can change this later in the UI.
* `description: str`

  A short blurb about the project.

**Return Value:**

A `RIMEProject` that describes the created project.
Its `project_id` attribute can be used in `start_stress_test()` and `list_stress_test_jobs()`.

**Example:**

```Python
project = rime_client.create_project(name='foo', description='bar')
```

### `list_stress_test_jobs()`

Query the backend for a list of jobs filtered by status and project ID.
This is a good way to recover `RIMEStressTestJob` objects.
Note that this only returns jobs from the last two days, because the time-to-live of job objects in the backend is set at two days.

**Arguments:**

* `status_filters: Optional[List[str]] = None`

  Select jobs by a union of statuses.
  If this is omitted, jobs will not be filtered by status.
  Acceptable values are in the following array:
  ```Python
  ['UNKNOWN_JOB_STATUS', 'PENDING', 'RUNNING', 'FAILING', 'SUCCEEDED']
  ```
* `project_id: Optional[str] = None`

  Select jobs by project.
  If this is omitted, jobs from across different projects will be returned.

**Return Value:**

A list of `RIMEStressTestJob` objects.
These are not guaranteed to be in any sorted order.

**Example:**
```Python
# Get all running and succeeded jobs for project 'foo'
jobs = rime_client.list_stress_test_jobs(status_filters=['RUNNING', 'SUCCEEDED'], project_id='foo')
```

## RIMEStressTestJob

This object provides an interface for monitoring the status of a stress test job in the RIME backend.

### `get_status()`

Query the RIME backend for the job's status.
This includes flags for blocking until the job is complete and printing information to `stdout`.
This method can help with monitoring the progress of stress test jobs, because it prints out helpful information such as running time and the progress of the test run.

**Arguments:**

* `verbose: bool = False`

  Whether to print additional status information to `stdout`.
  If this flag is enabled and the job status is `'SUCCEEDED'` or `'FAILING'`, the logs of the testing engine will be dumped to `stdout` to help with debuggability.
  Note that this logs have no strict form and will be subject to significant change in future versions.
* `wait_until_finish: bool = False`

  Whether to block until the job status is `'SUCCEEDED'` or `'FAILING'`.
  If `verbose` is enabled too, information about the job including running time and progress will be printed to `stdout` every `poll_rate_sec`.
* `poll_rate_sec: float = 5.0`

  How often to ping the RIME backend services for the status of the job.
  Units are in seconds.

**Return Value:**

A dictionary representing the status of the `RIMEStressTestJob`.
```Python
{
  "name": str
  "type": str
  "status": str
  "start_time_secs": int64
  "running_time_secs": double
}
```
`type` will be an element in the following array:
```Python
['MODEL_STRESS_TEST', 'UNKNOWN_JOB_TYPE']
```
`status` will be an element in the following array:
```Python
['UNKNOWN_JOB_STATUS', 'PENDING', 'RUNNING', 'FAILING', 'SUCCEEDED']
```

**Example:**

```Python
# Block until this job is finished and dump monitoring info to stdout.
job_status = job.get_status(verbose=True, wait_until_finish=True)
```

### `get_result_csv()`

This method constructs a CSV file of stress testing results that were produced by the RIME stress testing job.
It allows RIME users to programmatically parse results and make decisions based on RIME evaluations of their model and dataset.
Note this method will only succeed if the job has status `'SUCCEEDED'`.

**Arguments:**

* `filepath: str`

  Path to where the CSV results will be written.
  Beware that this overwrites existing files.
* `version: Optional[str] = None`

  Semantic version of the CSV to be returned.
  This allows users to pin the version of the results CSV, which is helpful if you write any code on top of RIME data.
  If you upgrade the SDK and do not pin the version in your code, it may break because the CSV is not guaranteed to be stable across versions.
  The latest version of the CSV will be returned by default.

**Example:**

```Python
# Wait until the job has finished, since this method only works on SUCCEEDED jobs.
job.get_status(verbose=True, wait_until_finish=True)

# Dump the CSV of results in `results.csv`.
# Pin the version to RIME version 0.12.0.
job.get_result_csv("results.csv", version="0.12.0")
```

## RIMEProject

This object describes a project in the RIME backend.

**Attributes:**

* `project_id: str`

  How to refer to the project in the backend.
  Use this attribute to specify the project for the backend in `start_stress_test_job()` and `list_stress_test_jobs()`.
* `name: str`
* `description: str`

## CustomImage

This allows users to specify custom Docker images on which their stress test jobs will be run.
An example use case is if you need a particular version of a library or an additional dependency to run your model.

*Note: this is deprecated as of RIME V13.
Managed Images should be used instead.
See `create_managed_image` and `list_managed_images` for more information.*

**Attributes:**

* `name: str`

  The name and tag of the Docker image.
  This should specify exactly which image to pull.
* `pull_secret: CustomImage.PullSecret`

  If you need a particular registry credential to pull the specified Docker image, add the pull secret field to tell the RIME backend cluster which secret to use.
  This secret will already need to be stored in the cluster.

**Example:**

```Python
custom_image = CustomImage(name="company/testing-engine-with-xgboost:latest", pull_secret=CustomImage.PullSecret(name="my_secret_name"))
```
