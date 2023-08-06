# awslayer-manager

This is a simple tool that helps you build and upload your project requirements as an AWS Lambda Layer. It extracts
the requirements from your Pipfile and installs them into a separate directory which it is then deployed from. This
package also supports working with the high performance `mysqlclient` library by compiling it inside a docker container
that closely mimics the AWS Lambda environment and deploying it with the layer.

## Installation

To install this package, run

```bash
pip install awslayer-manager
```

### Requirements

- Requires your project to be using the `Serverless` framework.
- This package requires `Docker` to build requirements to avoid compilation issues.

## Running

To initialize the layer run

```bash
awslayer
```

in the project directory. This will extract requirements from your Pipfile and create a serverless.yml inside the layer
directory. Once the layer is initialized, it will install all the requirements inside the `layers/package` directory and
deploy it using `sls deploy` the layer to the specified environment (dev by default).

To change the deployment environment use the `--env` option. Currently supports `dev`, `stage`, and `prod` environments.

Once that is done, add the following (omit square brackets) for each function in your project's serverless.yml:

```YAML
functions:
  func-name:
    handler: src/handler.func-name
    layers:
      - "${cf:[stack-name].[ServiceName]LayerLambdaLayerQualifiedArn}"
```

where you can find the "[ServiceName]LayerLambdaLayerQualifiedArn" identifier in the CloudFormation stack.

**NOTE:** This package will create a `.layer` directory inside your project which I recommend adding to your .gitignore
file as it is fairly heavy (depending on the size of your requirements). The script, however, will try to clean up
to the best of its ability.

## Contributing

Pull requests are welcome.
