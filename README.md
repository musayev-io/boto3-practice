# Boto 3 Notes

## High-Level Overview

Boto 3 is a AWS SDK for Python 3. Boto 3 is built atop of a library called Botocore, which is shared by the AWS CLI. Botocore provides the low level clients, session, and credential & configuration data. Boto 3 builds on top of Botocore by providing its own session, resources and collections.

### Major Components of Boto 3

-   **Resources**: a high level, object oriented interface
-   **Collections**: a tool to iterate and manipulate groups of resources
-   **Clients**: low level service connections
-   **Paginators**: automatic paging of responses
-   **Waiters**: a way to block until a certain state has been reached

### Credentials

Unless you're doing basic testing using default AWS resources, you'll want to setup a custom-tailored _**Session**_ to modify the region/credentials for the session and use it call the Client/Resource.

> A _**Session**_ stores configuration state and allows you to create service clients and resources.

_**Session Class**_

```python
    class boto3.session.Session(aws_access_key_id=None,
                                 aws_secret_access_key=None,
                                 aws_session_token=None,
                                 region_name=None,
                                 botocore_session=None,
                                 profile_name=None)
```

You can use a _**Session**_ on **Clients** and **Resources**:

```python
    client(service_name, region_name=None, api_version=None,
           use_ssl=True, verify=None, endpoint_url=None,
           aws_access_key_id=None, aws_secret_access_key=None,
           aws_session_token=None, config=None)
```

Bring these two together and you get this:

```python
    import boto3

    aws_access_key_id = '<AWS_ACCESS_KEY_ID>'
    aws_secret_access_key = '<AWS_SECRET_ACCESS_KEY>'
    region_name = 'us-east-1'

    ec2 = boto3.resource('ec2',
                       aws_access_key_id=aws_access_key_id,
                       aws_secret_access_key=aws_secret_access_key,
                       region_name=region_name)
```

Resources:

-   [Session Reference](https://boto3.readthedocs.io/en/latest/reference/core/session.html)
-   [StackOverflow](https://stackoverflow.com/questions/42809096/difference-in-boto3-between-resource-client-and-session/42818143#42818143)

### Service Documentation

Documentation on how to use the **Clients** and **Services** can be found in the [Service Documentation](http://boto3.readthedocs.io/en/latest/reference/services/index.html).

> The link hierarchy is flat. Everything under **Client** pertains to Client Configuration. Same goes for **Service Resource**

## Clients

Details about Clients can be found in [Low-level Clients](https://boto3.readthedocs.io/en/latest/guide/clients.html)

-   All service operations are supported by clients
-   Parameters must be sent as keyword arguments. They will not work as positional arguments.
-   Response are returned as Python dictionaries.
-   It's our responsibility to traverse/process the keys for the dat we need
    -   _Responses may not always included the expected data_  

### Extracting Data

```Python
client_instance = ec2client.run_instances(
    ImageId='ami-30041c53',
    KeyName='Keys',
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro')
```

Running `client_instance` will produce the following dictionary:

        {'Groups': [],
         'Instances': [{'AmiLaunchIndex': 0,
           'Architecture': 'x86_64',
           'BlockDeviceMappings': [],
           'ClientToken': '',
           'EbsOptimized': False,
           'Hypervisor': 'xen',
           'ImageId': 'ami-30041c53',
           'InstanceId': 'i-0e3a125b86073f341',
           etc...

To extract data, you will need to run: `client_instance['Instances'][0]['InstanceId']` to return `i-0e3a125b86073f341`

## Resources

Details about **Resources** can be found in [Resources](https://boto3.readthedocs.io/en/latest/guide/resources.html)

According to the documentation, _"Resources represent an object-oriented interface to Amazon Web Services (AWS). They provide a higher-level abstraction than the raw, low-level calls made by service clients."_

-   This means **Resources** can do the same things as **Clients**, but their output is easier to consume than manually traversing dictionary key:value within **Clients**.

### Identifiers, Attributes, References, Actions, & Collections

-   **Identifiers**

    -   From Documentation: _Properties of a resource are set upon instantiation of the resource._
        -   This means when a Resource is initialized, it's given a unique ID. Use this ID to make subsequent Attribute and Action calls.

-   **Attributes**

    -   From Documentation: _Provide access to the properties of a resource. Attributes are lazy-loaded the first time one is accessed via the load() method._
        -   Use the Resource's ID to gather Attributes belonging to the Resource
            -   **IN**: `ec2_example_resource.Instance('i-a09sdf3j').id`
            -   **OUT**: `ami-12345abcdef`

-   **References**                       

    -   From Documentation: _Related resource instances that have a belongs-to relationship._
        -   References are methods that belong to the Python instance, not the Boto Resource's ID.
            -   **IN**: `resource_isntance[0].vpc.id`
            -   **OUT**: `vpc-12345abcdef`


-   **Actions**  

    -   From Documentation: _Call operations on resources. They may automatically handle the passing in of arguments set from identifiers and some attributes._
        -   Performs an Action on the Resource, e.g., (start/shutdown a host)


-   **Collections**

    -   From Documentation: _Provide an interface to iterate over and manipulate groups of resources_
        -   Used to iterate over all the values of a given Resource, e.g., (All the snapshots of an EBS volume, the subnets that belong in a VPC)

### Extracting Data

```python
resource_instance = ec2resource.create_instances(
    ImageId='ami-30041c53',
    KeyName='Keys',
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro')
```

Running `resource_instance` will produce the following list: `[ec2.Instance(id='i-0afb49cac524f3191')]`

To extract data, you will need to run: `resource_instance[0].id` to return `i-0e3a125b86073f341`
