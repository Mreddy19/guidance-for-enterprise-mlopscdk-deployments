Platform setup
=========================================================

To get started you will need and AWS account where this platform hasn't been installed previously. Here are main steps :

* :ref:`started:Deploy the Infrastructure`: you will need Admin privileges in your AWS account to deploy the infrastructure using CloudFormation. The process takes approximately 1 hour and involves deployment of the necessary infrastructure. It is important to **configure SSO** as the roles during the infrastructure deployment need to be linked to users in your environment. This will depend on how SSO is set up in your organisation.
* :ref:`started:Create a SageMaker Project`: The Data Science Admin logs to SageMaker Studio through AWS console and creates an isolated SageMaker Project for data science work.
* :ref:`started:Create a SageMaker Studio User`: Data Science Admin logs into the AWS console to create a new SageMaker Studio user using `AWS Service Catalog <https://aws.amazon.com/servicecatalog/>`_ and links the new user to the project created in the previous step. 
* :ref:`started:Launch SageMaker Studio as Data Science User`: A Data Scientist logs into the AWS console, accesses SageMaker user to which they have access, launches a SageMaker Studio session and begins working on a data science project that was defined for them by the Data Science Admin in the previous step.


Deploy The Infrastructure
-------------------------

TASK: Deploy the initial infrastructure using CloudFormation template. 

Deployment can be initiated from either the ``main`` or the ``develop`` branches. The stable version of the deployment is on the ``main`` branch. The latest development version of the deployment is on the ``develop`` branch. 

Deploy From The ``main`` Branch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Click on the "Launch Stack" button below corresponding to your AWS region.
You may then be required to log into the target AWS account in which the
infrastructure will be deployed.


.. list-table::
   :widths: 25 25 50
   :header-rows: 1

   * - Region name
     - Region code
     - Launch

   * - US East (N. Virginia)
     - us-east-1
     - |useast1|_

   * - US East (Ohio)
     - us-east-2
     - |useast2|_

   * - US West (Oregon)
     - us-west-2
     - |uswest2|_

   * - Asia Pacific (Mumbai)
     - ap-south-1
     - |apsouth1|_

   * - Asia Pacific (Singapore)
     - ap-southeast-1
     - |apsoutheast1|_

   * - Asia Pacific (Sydney)
     - ap-southeast-2
     - |apsoutheast2|_

   * - Asia Pacific (Tokyo)
     - ap-northeast-1
     - |apnortheast1|_

   * - EU (Frankfurt)
     - eu-central-1
     - |eucentral1|_

   * - EU (Ireland)
     - eu-west-1
     - |euwest1|_

   * - Europe (London)
     - eu-west-2
     - |euwest2|_

   * - Europe (Paris)
     - eu-west-3
     - |euwest3|_

   * - Europe (Milan)
     - eu-south-1
     - |eusouth1|_

   * - Europe (Stockholm)
     - eu-north-1
     - |eunorth1|_

.. |useast1| image:: images/cloudformation-launch-stack.png
.. _useast1: https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/quickcreate?templateUrl=https%3A%2F%2Faws-enterprise-mlops-platform.s3.amazonaws.com%2Fmlops_entry_point.yaml&stackName=aws-mlops-accelerator-stack&param_BucketName=aws-enterprise-mlops-platform&param_CostCenter=12345

.. |useast2| image:: images/cloudformation-launch-stack.png
.. _useast2: https://us-east-2.console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/quickcreate?templateUrl=https%3A%2F%2Faws-enterprise-mlops-platform.s3.amazonaws.com%2Fmlops_entry_point.yaml&stackName=aws-mlops-accelerator-stack&param_BucketName=aws-enterprise-mlops-platform&param_CostCenter=12345

.. |uswest2| image:: images/cloudformation-launch-stack.png
.. _uswest2: https://us-west-2.console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/quickcreate?templateUrl=https%3A%2F%2Faws-enterprise-mlops-platform.s3.amazonaws.com%2Fmlops_entry_point.yaml&stackName=aws-mlops-accelerator-stack&param_BucketName=aws-enterprise-mlops-platform&param_CostCenter=12345

.. |apsouth1| image:: images/cloudformation-launch-stack.png
.. _apsouth1: https://ap-south-1.console.aws.amazon.com/cloudformation/home?region=ap-south-1#/stacks/quickcreate?templateUrl=https%3A%2F%2Faws-enterprise-mlops-platform.s3.amazonaws.com%2Fmlops_entry_point.yaml&stackName=aws-mlops-accelerator-stack&param_BucketName=aws-enterprise-mlops-platform&param_CostCenter=12345

.. |apsoutheast1| image:: images/cloudformation-launch-stack.png
.. _apsoutheast1: https://ap-southeast-1.console.aws.amazon.com/cloudformation/home?region=ap-southeast-1#/stacks/quickcreate?templateUrl=https%3A%2F%2Faws-enterprise-mlops-platform.s3.amazonaws.com%2Fmlops_entry_point.yaml&stackName=aws-mlops-accelerator-stack&param_BucketName=aws-enterprise-mlops-platform&param_CostCenter=12345

.. |apsoutheast2| image:: images/cloudformation-launch-stack.png
.. _apsoutheast2: https://ap-southeast-2.console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/quickcreate?templateUrl=https%3A%2F%2Faws-enterprise-mlops-platform.s3.amazonaws.com%2Fmlops_entry_point.yaml&stackName=aws-mlops-accelerator-stack&param_BucketName=aws-enterprise-mlops-platform&param_CostCenter=12345

.. |apnortheast1| image:: images/cloudformation-launch-stack.png
.. _apnortheast1: https://ap-northeast-1.console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/quickcreate?templateUrl=https%3A%2F%2Faws-enterprise-mlops-platform.s3.amazonaws.com%2Fmlops_entry_point.yaml&stackName=aws-mlops-accelerator-stack&param_BucketName=aws-enterprise-mlops-platform&param_CostCenter=12345

.. |eucentral1| image:: images/cloudformation-launch-stack.png
.. _eucentral1: https://eu-central-1.console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/quickcreate?templateUrl=https%3A%2F%2Faws-enterprise-mlops-platform.s3.amazonaws.com%2Fmlops_entry_point.yaml&stackName=aws-mlops-accelerator-stack&param_BucketName=aws-enterprise-mlops-platform&param_CostCenter=12345

.. |euwest1| image:: images/cloudformation-launch-stack.png
.. _euwest1: https://eu-west-1.console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/quickcreate?templateUrl=https%3A%2F%2Faws-enterprise-mlops-platform.s3.amazonaws.com%2Fmlops_entry_point.yaml&stackName=aws-mlops-accelerator-stack&param_BucketName=aws-enterprise-mlops-platform&param_CostCenter=12345

.. |euwest2| image:: images/cloudformation-launch-stack.png
.. _euwest2: https://eu-west-2.console.aws.amazon.com/cloudformation/home?region=eu-west-2#/stacks/quickcreate?templateUrl=https%3A%2F%2Faws-enterprise-mlops-platform.s3.amazonaws.com%2Fmlops_entry_point.yaml&stackName=aws-mlops-accelerator-stack&param_BucketName=aws-enterprise-mlops-platform&param_CostCenter=12345

.. |euwest3| image:: images/cloudformation-launch-stack.png
.. _euwest3: https://eu-west-3.console.aws.amazon.com/cloudformation/home?region=eu-west-3#/stacks/quickcreate?templateUrl=https%3A%2F%2Faws-enterprise-mlops-platform.s3.amazonaws.com%2Fmlops_entry_point.yaml&stackName=aws-mlops-accelerator-stack&param_BucketName=aws-enterprise-mlops-platform&param_CostCenter=12345

.. |eusouth1| image:: images/cloudformation-launch-stack.png
.. _eusouth1: https://eu-south-1.console.aws.amazon.com/cloudformation/home?region=eu-south-1#/stacks/quickcreate?templateUrl=https%3A%2F%2Faws-enterprise-mlops-platform.s3.amazonaws.com%2Fmlops_entry_point.yaml&stackName=aws-mlops-accelerator-stack&param_BucketName=aws-enterprise-mlops-platform&param_CostCenter=12345

.. |eunorth1| image:: images/cloudformation-launch-stack.png
.. _eunorth1: https://eu-north-1.console.aws.amazon.com/cloudformation/home?region=eu-north-1#/stacks/quickcreate?templateUrl=https%3A%2F%2Faws-enterprise-mlops-platform.s3.amazonaws.com%2Fmlops_entry_point.yaml&stackName=aws-mlops-accelerator-stack&param_BucketName=aws-enterprise-mlops-platform&param_CostCenter=12345

Deploy From The ``develop`` Branch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Click on the "Launch Stack" button below corresponding to your AWS region.
You may then be required to log into the target AWS account in which the
infrastructure will be deployed.

.. list-table::
   :header-rows: 1

   * - Region name
     - Region code
     - Launch

   * - US East (N. Virginia)
     - us-east-1
     - |useast1dev|_

   * - US East (Ohio)
     - us-east-2
     - |useast2dev|_

   * - US West (Oregon)
     - us-west-2
     - |uswest2dev|_

   * - Asia Pacific (Mumbai)
     - ap-south-1
     - |apsouth1dev|_

   * - Asia Pacific (Singapore)
     - ap-southeast-1
     - |apsoutheast1dev|_

   * - Asia Pacific (Sydney)
     - ap-southeast-2
     - |apsoutheast2dev|_

   * - Asia Pacific (Tokyo)
     - ap-northeast-1
     - |apnortheast1dev|_

   * - EU (Frankfurt)
     - eu-central-1
     - |eucentral1dev|_

   * - EU (Ireland)
     - eu-west-1
     - |euwest1dev|_

   * - Europe (London)
     - eu-west-2
     - |euwest2dev|_

   * - Europe (Paris)
     - eu-west-3
     - |euwest3dev|_

   * - Europe (Milan)
     - eu-south-1
     - |eusouth1dev|_

   * - Europe (Stockholm)
     - eu-north-1
     - |eunorth1dev|_


.. |useast1dev| image:: images/cloudformation-launch-stack.png
.. _useast1dev: https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/quickcreate?templateUrl=https%3A%2F%2Faws-enterprise-mlops-platform-develop.s3.amazonaws.com%2Fmlops_entry_point.yaml&stackName=aws-mlops-accelerator-stack&param_BucketName=aws-enterprise-mlops-platform-develop&param_CostCenter=12345&param_BranchName=main

.. |useast2dev| image:: images/cloudformation-launch-stack.png
.. _useast2dev: https://us-east-2.console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/quickcreate?templateUrl=https%3A%2F%2Faws-enterprise-mlops-platform-develop.s3.amazonaws.com%2Fmlops_entry_point.yaml&stackName=aws-mlops-accelerator-stack&param_BucketName=aws-enterprise-mlops-platform-develop&param_CostCenter=12345&param_BranchName=main

.. |uswest2dev| image:: images/cloudformation-launch-stack.png
.. _uswest2dev: https://us-west-2.console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/quickcreate?templateUrl=https%3A%2F%2Faws-enterprise-mlops-platform-develop.s3.amazonaws.com%2Fmlops_entry_point.yaml&stackName=aws-mlops-accelerator-stack&param_BucketName=aws-enterprise-mlops-platform-develop&param_CostCenter=12345&param_BranchName=main

.. |apsouth1dev| image:: images/cloudformation-launch-stack.png
.. _apsouth1dev: https://ap-south-1.console.aws.amazon.com/cloudformation/home?region=ap-south-1#/stacks/quickcreate?templateUrl=https%3A%2F%2Faws-enterprise-mlops-platform-develop.s3.amazonaws.com%2Fmlops_entry_point.yaml&stackName=aws-mlops-accelerator-stack&param_BucketName=aws-enterprise-mlops-platform-develop&param_CostCenter=12345&param_BranchName=main

.. |apsoutheast1dev| image:: images/cloudformation-launch-stack.png
.. _apsoutheast1dev: https://ap-southeast-1.console.aws.amazon.com/cloudformation/home?region=ap-southeast-1#/stacks/quickcreate?templateUrl=https%3A%2F%2Faws-enterprise-mlops-platform-develop.s3.amazonaws.com%2Fmlops_entry_point.yaml&stackName=aws-mlops-accelerator-stack&param_BucketName=aws-enterprise-mlops-platform-develop&param_CostCenter=12345&param_BranchName=main

.. |apsoutheast2dev| image:: images/cloudformation-launch-stack.png
.. _apsoutheast2dev: https://ap-southeast-2.console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/quickcreate?templateUrl=https%3A%2F%2Faws-enterprise-mlops-platform-develop.s3.amazonaws.com%2Fmlops_entry_point.yaml&stackName=aws-mlops-accelerator-stack&param_BucketName=aws-enterprise-mlops-platform-develop&param_CostCenter=12345&param_BranchName=main

.. |apnortheast1dev| image:: images/cloudformation-launch-stack.png
.. _apnortheast1dev: https://ap-northeast-1.console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/quickcreate?templateUrl=https%3A%2F%2Faws-enterprise-mlops-platform-develop.s3.amazonaws.com%2Fmlops_entry_point.yaml&stackName=aws-mlops-accelerator-stack&param_BucketName=aws-enterprise-mlops-platform-develop&param_CostCenter=12345&param_BranchName=main

.. |eucentral1dev| image:: images/cloudformation-launch-stack.png
.. _eucentral1dev: https://eu-central-1.console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/quickcreate?templateUrl=https%3A%2F%2Faws-enterprise-mlops-platform-develop.s3.amazonaws.com%2Fmlops_entry_point.yaml&stackName=aws-mlops-accelerator-stack&param_BucketName=aws-enterprise-mlops-platform-develop&param_CostCenter=12345&param_BranchName=main

.. |euwest1dev| image:: images/cloudformation-launch-stack.png
.. _euwest1dev: https://eu-west-1.console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/quickcreate?templateUrl=https%3A%2F%2Faws-enterprise-mlops-platform-develop.s3.amazonaws.com%2Fmlops_entry_point.yaml&stackName=aws-mlops-accelerator-stack&param_BucketName=aws-enterprise-mlops-platform-develop&param_CostCenter=12345&param_BranchName=main

.. |euwest2dev| image:: images/cloudformation-launch-stack.png
.. _euwest2dev: https://eu-west-2.console.aws.amazon.com/cloudformation/home?region=eu-west-2#/stacks/quickcreate?templateUrl=https%3A%2F%2Faws-enterprise-mlops-platform-develop.s3.amazonaws.com%2Fmlops_entry_point.yaml&stackName=aws-mlops-accelerator-stack&param_BucketName=aws-enterprise-mlops-platform-develop&param_CostCenter=12345&param_BranchName=main

.. |euwest3dev| image:: images/cloudformation-launch-stack.png
.. _euwest3dev: https://eu-west-3.console.aws.amazon.com/cloudformation/home?region=eu-west-3#/stacks/quickcreate?templateUrl=https%3A%2F%2Faws-enterprise-mlops-platform-develop.s3.amazonaws.com%2Fmlops_entry_point.yaml&stackName=aws-mlops-accelerator-stack&param_BucketName=aws-enterprise-mlops-platform-develop&param_CostCenter=12345&param_BranchName=main

.. |eusouth1dev| image:: images/cloudformation-launch-stack.png
.. _eusouth1dev: https://eu-south-1.console.aws.amazon.com/cloudformation/home?region=eu-south-1#/stacks/quickcreate?templateUrl=https%3A%2F%2Faws-enterprise-mlops-platform-develop.s3.amazonaws.com%2Fmlops_entry_point.yaml&stackName=aws-mlops-accelerator-stack&param_BucketName=aws-enterprise-mlops-platform-develop&param_CostCenter=12345&param_BranchName=main

.. |eunorth1dev| image:: images/cloudformation-launch-stack.png
.. _eunorth1dev: https://eu-north-1.console.aws.amazon.com/cloudformation/home?region=eu-north-1#/stacks/quickcreate?templateUrl=https%3A%2F%2Faws-enterprise-mlops-platform-develop.s3.amazonaws.com%2Fmlops_entry_point.yaml&stackName=aws-mlops-accelerator-stack&param_BucketName=aws-enterprise-mlops-platform-develop&param_CostCenter=12345&param_BranchName=main

    This deploys a cloudformation stack named 'aws-mlops-accelerator-stack' which in turn deploys the following stacks to deploy the project's initial infrastructure:
    stackset-execution-role,
    stackset-admin-role,
    deploy-infra-stack,
    sm-tag-lambda-stack,
    sc-project-stack,
    AWS Enterprise MLOps Platform uses `AWS CodeArtifact <https://aws.amazon.com/codeartifact/>`_ to serve as a prive PyPi server.  With this in mind, please ensure you are deploying into a `region that includes a CodeArtifact endpoint. <https://docs.aws.amazon.com/general/latest/gr/codeartifact.html>`_

Create a SageMaker Project
--------------------------

TASK: as a Data Science Admin create a new data science  project and the associated resources.

This step should be performed by a data science admin in your organisation at the beginning of each new project. Notice, that the SageMaker-provided project templates have been disabled by this deployment.

After the project's initial infrastructure has been deployed, you will create a custom project in SageMaker Studio upon assuming Data Science Role. You will choose the type of the data science problem (supervised or unspervised), type of inference (batch or real time) and you will associate mandatory (CostCenter) and custom tags with the project. The CostCenter tag is used for tracking the spending associated with the project. 

The steps are outlined below:

1. Log into AWS Console with the Data Science Admin role. Follow the link `AWS console <https://signin.aws.amazon.com/switchrole>`_ to assume the Data Science Admin role. The role has been created for you during the deployment. The role name has the following pattern:  *<region>-datascience-admin-<account_id>*). You might find it helpful to first navigate to IAM in AWS Console in order to retrieve the role name and assume it using `AWS console <https://signin.aws.amazon.com/switchrole>`_ link. 

2. Once you assume the role, navigate to Amazon SageMaker in AWS Console. On the left side panel select Domains. Click on the created domain (domain name will have the following pattern *<region>-studio-domain*). This will open **User profiles** tab for the domain information page. In the **User profiles** tab click on the Launch button next to *ds-admin* user to launch Studio.

.. image:: images/domains.png
   :height: 400px
   :scale: 100 %
   :alt: sagemaker domains page
   :align: center

1. Once SageMaker Studio UI is loaded click on the  Deployments->Projects menu and then the `Create project`  button. Next select the `Organization templates` tab and then the custom resource named SageMaker Project. In the lower-right hand corner, Select project template to initiate project creation.

2.  In this step we will provide parameters to our custom SageMaker project. You can optionally add other tags to the project. When ready, click `Create project` to complete the project creation. The animation below demonstrates the steps that need to be taken the by Data Science Admin in SageMaker Studio. 

.. image:: images/ds_admin_create_project.gif
   :height: 700px
   :scale: 100 %
   :alt: project params
   :align: center

|

    Important: Creation in SageMaker Studio will initiate execution of `<sagemaker_project_name>_project_pipeline` CodePipeline. The project will become available once the pipeline execution is completed. 

|

Create a SageMaker Studio User
-------------------------------

TASK: As a Data Science Admin, create a SageMaker Studio user for your project. 

After the `<sagemaker_project_name>_project_pipeline` executes, this step is performed by a data science administrator in your organization for each user who will work on a project created in the previous section. There could be 1 or many users working on a particular project and having access to its resources. 

Unlike creation of the SageMaker Studio Project, which is accomplished by the Data Science Admin in SageMaker Studio, association of the users with the newly created project is accomplished in AWS Service Catalog. In the Service Catalog the Data Science Admin will link the project created in the previous section with a specific user.

The steps are outlined below:

1. If not logged in as a Data Science admin log into AWS Console as the Data Science Admin role. Follow the link `AWS console <https://signin.aws.amazon.com/switchrole>`_ to assume the Data Science Admin role. Navigate to AWS Service Catalog in the console.
2. Select `Products` from the left-hand pane. You will see a product representing a SageMaker Studio User for the project you just created.  In this example, the project name is "mlops-demo-project" and so the Product name is "mlops-demo-project SageMaker Studio User".
3.  Select the product representing the SM Studio User for your project and click `Launch product`.

.. image:: images/project_admin_create_user.png
   :height: 750px
   :scale: 80 %
   :alt: project params
   :align: center

4.  In this step the Data Science Admin will customize the newly created project with Parameters. The most important customization is the `UserEmail` parameter. Enter the email of the Data Science User that will be associated with this project and will have access to its resources.

For our SageMaker Studio user, be sure to update the `UserEmail` field with the email address of the Data Scientist that will be using the SM Studio User.
|

    Note: Add note here about `attribute-based access control <https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction_attribute-based-access-control.html>`_

.. image:: images/project_admin_create_user2.png
   :height: 900px
   :scale: 100 %
   :alt: project params
   :align: center

|
    Important: Once the product is launched, it will initiate `<sagemaker_project_name>_<username>_user_pipeline` Code Pipeline execution. Wait for the CodePipeline execution to complete before accessing the new SageMaker user. Once the pipeline execution is completed the new SageMaker user will be available in SageMaker Studio.

|

Launch SageMaker Studio as Data Science User
----------------------------------------------

TASK: as a Data Scientist, use SageMaker Studio to begin model development.

Once the data science admin in your organisation provisions the project and links a user to the project, this user (data scientist(s) in your organisation) can begin working on the problem: perform data exploration, data cleaning, building a model and fine-tuning the hyperparameters. In this step we will show how a Data Science User will login to SageMaker console. 


1. Log into AWS Console with the Data Science User role. Follow the link `AWS console <https://signin.aws.amazon.com/switchrole>`_ to assume the Data Science Admin role. The role has been created for you during the deployment. The role name has the following pattern:  *<region>-datascientist-<account_id>*). You might find it helpful to first navigate to IAM in AWS Console in order to retrieve the role name and assume it using `AWS console <https://signin.aws.amazon.com/switchrole>`_ link. 
2.  Navigate to SageMaker Studio, click on Domains, then on the domain *<region>-studio-domain*. This will open the tab `User profiles`. The SageMaker Studio User will have the name "<email alias>-<project name>".  In this example, our SageMaker project is "mlops-demo-project" and our user email address is "fakename@example.com", so our SM Studio User is "fakename-mlops-demo-project".  Select `Launch app` and then `Studio` for this user to launch SageMaker Studio and get started with model development. This will launch SageMaker Studio UI.

.. image:: images/project_admin_create_user3.png
   :height: 650px
   :scale: 80 %
   :alt: project params
   :align: center


In the next section, we will demonstrate how a Data Science User will interact with the platform to develop and deploy a model.

