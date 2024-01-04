import os
from itertools import count

from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import ECR, LambdaFunction
from diagrams.aws.devtools import Codebuild, Codecommit, Codepipeline
from diagrams.aws.management import (
    Cloudformation,
    CloudformationStack,
    CloudformationTemplate,
    ParameterStore,
    ServiceCatalog,
)
from diagrams.aws.ml import Sagemaker
from diagrams.aws.security import KMS, IAMRole
from diagrams.aws.storage import S3, SimpleStorageServiceS3BucketWithObjects
from diagrams.custom import Custom
from diagrams.generic.blank import Blank

PWD = os.path.dirname(os.path.abspath(__file__))


def make_dot(*args, **kwargs):
    return Blank(*args, shape="point", height="0.075", **kwargs)


def make_vpc_endpoint(*args, **kwargs):
    return Custom(
        *args, os.path.join(PWD, "images", "aws-endpoint.png"), **kwargs
    )


def make_codeartifact(*args, **kwargs):
    return Custom(
        *args, os.path.join(PWD, "images", "aws-codeartifact.png", **kwargs)
    )


def make_high_level_architecture(
    fn="images/component_reference/overall_architecture.png",
):
    """ """

    graph_attr = {
        "splines": "polylines"
        # "splines": "spline"
    }

    _filename = os.path.splitext(fn)[0]
    _outformat = os.path.splitext(fn)[1].lstrip(".").lower()

    diagram_kwargs = {
        "name": "",
        "filename": _filename,
        "outformat": _outformat,
        "show": False,
        # "curvestyle": "curved",
        # "curvestyle": "ortho",
        # "curvestyle": "splines",
        "direction": "LR",
        "graph_attr": graph_attr,
    }

    resource_names = [
        "S3",
        "KMS",
        "SageMaker API",
        "SageMaker Runtime",
        "SageMaker Feature Store Runtime",
        "SageMaker Studio",
        "CodeCommit",
        "CodePipeline",
        "CodeArtifact",
        "SSM",
        "Service Catalog",
        "CloudWatch",
        "EC2",
        "STS",
        "ECR",
    ]

    account_id = "<ACCOUNT_ID>"

    with Diagram(**diagram_kwargs):
        project_admin_role = IAMRole("ProjectAdmin")
        ds_admin_role = IAMRole("DataScienceAdmin")
        ds_user_role = IAMRole("DataScientist")
        infra_template = CloudformationTemplate("1-infra.yaml")

        with Cluster(
            f"mlops-infra-stack\naccount id: {account_id}",
            graph_attr={
                "bgcolor": "transparent",
            },
        ):
            with Cluster("VPC"):
                with Cluster("PrivateSubnet1 & PrivateSubnet2"):
                    with Cluster("SecurityGroup"):
                        with Cluster("StudioDomain"):
                            Sagemaker("StudioDomain")
                            ds_admin_app = Sagemaker("ds-admin\n(App)")

                            with Cluster("project01"):
                                proj1 = ServiceCatalog(
                                    label="project01\nSageMaker\nStudio User\n"
                                    "(Product)"
                                )
                                create_proj1_user = Blank(
                                    label="(C) deploy user\nvia CloudFormation",
                                    labelloc="c",
                                    height="0.5",
                                )
                                u1p1_app = Sagemaker("user01-project01\n(App)")
                                u2p1_app = Sagemaker("user02-project01\n(App)")

                                (
                                    proj1 - Edge() - create_proj1_user
                                    >> Edge()
                                    >> [u1p1_app, u2p1_app]
                                )

                            with Cluster("project02"):
                                proj2 = Blank(
                                    label="...", labelloc="c", height="0.5"
                                )

                            create_project = Blank(
                                label="(B) deploy project\n via CloudFormation",
                                labelloc="c",
                                height="0.5",
                            )

                            ds_admin_app - Edge() - create_project >> [
                                proj1,
                                proj2,
                            ]

                    with Cluster("VPCEndpointSecurityGroup"):
                        vpc_endpoints = make_vpc_endpoint("VPC Endpoints")

                    with Cluster("Resources"):
                        resources = Blank(
                            "\n".join(resource_names),
                            labelloc="c",
                            width="3",
                            height="3",
                        )

            artifacts_bucket = SimpleStorageServiceS3BucketWithObjects(
                "ArtifactsBucket"
            )
            artifacts_bucket - resources
            (
                ds_admin_role
                >> Edge(
                    label="Use Case B:\nAs a Data Science Admin,\ncreate a "
                    "SageMaker Project",
                    style="dashed",
                )
                >> ds_admin_app
            )

            vpc_endpoints - Edge(penwidth="3") - resources
            (
                [
                    u1p1_app,
                    u2p1_app,
                ]
                - Edge(penwidth="3")
                - vpc_endpoints
            )

            mlops_codeartifact = make_codeartifact(
                "mlops-codeartifact-repository"
            )
            (
                mlops_codeartifact
                - Edge(label="python\npackages\n(private)")
                - resources
            )

            mlops_infra_stack = CloudformationStack("mlops-infra-stack")
            (
                project_admin_role
                >> Edge(
                    label="Use Case A:\nAs a Full-Stack Developer,\ndeploy the "
                    "initial infrastructure\nusing CloudFormation",
                    style="dashed",
                )
                >> infra_template
                >> mlops_infra_stack
            )

            (
                ds_admin_role
                - Edge(
                    label="Use Case C:\nAs a Data Science Admin,\nCreate a "
                    "User of the\nproject for a Data Scientist",
                    style="dashed",
                )
                >> proj1
            )

        use_case_dot = Blank(shape="point", height="0.05")
        use_case_d = Blank(
            label="Use Case D:\nAs a Data Scientist,\nUse the SageMaker Studio "
            "to\nstart model development",
            height="0.7",
        )
        use_case_e = Blank(
            label="Use Case E:\nAs a Data Scientist,\nTrigger the Model "
            "Building",
            height="0.7",
        )
        use_case_f = Blank(
            label="Use Case F:\nAs a Data Scientist,\nApprove the Model "
            "Deployment",
            height="0.7",
        )
        use_case_g = Blank(
            label="Use Case G:\nAs a Data Scientist,\nMonitor the Model "
            "Performance",
            height="0.7",
        )

        ds_user_role - Edge(style="dashed",) - [
            use_case_d,
            use_case_e,
            use_case_f,
            use_case_g,
        ] - Edge(style="dashed",) - use_case_dot - Edge(style="dashed") >> [
            u1p1_app,
            u2p1_app,
        ]

        with Cluster("project01 Resources"):
            proj1_bucket = SimpleStorageServiceS3BucketWithObjects(
                f"project01-{account_id}"
            )
            proj1_kms = KMS("alias: project01")
            proj1_ssm = ParameterStore("/mlops/projects/project01/*")
            proj1_codebuild = Codebuild("CodeBuild")
            proj1_sagemaker = Sagemaker("SageMaker")
            proj1_codepipeline = Codepipeline("CodePipeline")

        (
            use_case_f
            >> Edge(
                label="(F) Manually approve deployment\nvia AWS CodePipeline "
                "console",
            )
            >> proj1_codepipeline
        )

        with Cluster("project02 Resources"):
            proj2_resources = Blank(label="...", labelloc="c", height="0.5")

        resources - [
            proj1_bucket,
            proj1_kms,
            proj1_ssm,
            proj1_codepipeline,
            proj1_codebuild,
            proj1_sagemaker,
            proj2_resources,
        ]


def make_use_case_a(
    fn="images/component_reference/A_deploy_infrastructure.png",
):
    """Use-case A: As a Full-Stack Developer, deploy the initial infrastructure
    using CloudFormation (one-click deployment).

    """

    graph_attr = {
        "splines": "polylines"
        # "splines": "spline"
    }

    _filename = os.path.splitext(fn)[0]
    _outformat = os.path.splitext(fn)[1].lstrip(".").lower()

    diagram_kwargs = {
        "name": "",
        "filename": _filename,
        "outformat": _outformat,
        "show": False,
        # "curvestyle": "curved",
        # "curvestyle": "ortho",
        # "curvestyle": "splines",
        "direction": "LR",
        "graph_attr": graph_attr,
    }

    steps_a = count(1)

    with Diagram(**diagram_kwargs):
        role = IAMRole("FullStackDeveloper")

        # full_stack_dev = User("Full Stack\nDeveloper")
        template_yaml = CloudformationTemplate("mlops_entry_point.yaml")
        # git_repo = Custom("Git Repository", "images/logos/git-logo.png")
        entry_point_bucket = S3("aws-enterprise-mlops-platform")
        # entry_point_bucket_2 = S3("aws-enterprise-mlops-platform")
        deploy_infra_stack = CloudformationStack("deploy-infra-stack")
        deploy_stackset_admin_role_stack = CloudformationStack(
            "stackset-admin-role"
        )
        stackset_execution_role_stack = CloudformationStack(
            "stackset-execution-role"
        )
        codeartifact = Custom(
            "AWS CodeArtifact",
            os.path.join(PWD, "images/logos/aws-codeartifact.png"),
        )

        sm_tag_lambda_stack = CloudformationStack("sm-tag-lambda-stack")
        sc_project_stack = CloudformationStack("sc-project-stack")

        entry_point_bucket - template_yaml

        with Cluster(
            "AWS Management Console",
            graph_attr={
                "fontcolor": "red",
                "pencolor": "red",
                "style": "dashed",
                "bgcolor": "none",
            },
        ):
            cloudformation = Cloudformation("AWS CloudFormation")
            template_yaml >> Edge(xlabel="source") >> cloudformation
            (
                role
                >> Edge(
                    label="use CloudFormation\n" "via AWS Management Console"
                )
                >> cloudformation
            )

        with Cluster("mlops_entry_point.yaml stack"):
            stack = CloudformationStack("mlops_entry_point.yaml\nstack")
            artifacts_bucket = S3(
                "ArtifactsBucket\n" "{account_id}-{region}-mlops-artifacts"
            )
            ParameterStore("ArtifactsBucketParam")
            ParameterStore("InfraBranchNameParam")
            codepipeline_role = IAMRole("CodePipelineServiceRole")
            pipeline = Codepipeline(
                "MLOpsPlatformDeployPipeline\n"
                "mlops_platform_deploy\n(codepipeline)"
            )
            mlops_platform_repo = Codecommit(
                "MlopsPlatformRepo\naws-enterprise-mlops-platform\n"
                "(codecommit)"
            )
            init_mlops_platform_repo_project = Codebuild(
                "InitMlopsPlatformRepoProject\n"
                "init_mlops_platform_repo\n"
                "(codebuild-action)"
            )
            model_repo_project = Codebuild(
                "ModelRepoProject\nbuild_base_model_repo\n" "(codebuild-action)"
            )

            deploy_infra = Codebuild("deploy_infra\n(codebuild-action)")
            deploy_stackset_admin_role = Codebuild(
                "deploy_stackset_admin_role\n(codebuild-action)"
            )
            deploy_stackset_execution_role = Codebuild(
                "deploy_stackset_execution_role\n(codebuild-action)"
            )

            deploy_sm_tag_lambda = Codebuild(
                "deploy_sm_tag_lambda\n(codebuild-action)"
            )
            deploy_sc_supervised_learning_project = Codebuild(
                "deploy_sc_supervised_learning_project\n(codebuild-action)"
            )
            build_codeartifact_project = Codebuild(
                "build_codeartifact\n(codebuild-action)"
            )

            (
                cloudformation
                >> Edge(label=f"A.{next(steps_a)} one-click\ndeploy")
                >> stack
            )

            (
                entry_point_bucket
                >> Edge(
                    xlabel=f"A.{next(steps_a)} init. repo w/\n"
                    "aws-enterprise-mlops-\nplatform-init.zip",
                    style="solid",
                )
                >> mlops_platform_repo
            )

            (
                stack
                >> Edge(
                    label=f"A.{next(steps_a)} start pipeline", comment="xxxxx"
                )
                >> pipeline
            )

            (
                mlops_platform_repo
                >> Edge(
                    label=f"A.{next(steps_a)} source code\n" "from codecommit"
                )
                >> pipeline
            )

            build_stage = Blank(
                label=f"A.{next(steps_a)} Build stage",
                labelloc="",
                height="0.5",
                width="0.95",
            )

            (
                pipeline
                >> Edge(label="assume", style="dashed")
                >> codepipeline_role
            )
            pipeline - build_stage

            (
                build_stage
                >> Edge(xlabel=f"A.{next(steps_a)} action")
                >> init_mlops_platform_repo_project
            )

            (
                init_mlops_platform_repo_project
                >> Edge(label=f"A.{next(steps_a)} git push\nseedcode to repo.")
                >> mlops_platform_repo
            )

            (
                build_stage
                >> Edge(label=f"A.{next(steps_a)} action")
                >> model_repo_project
            )

            (
                model_repo_project
                >> Edge(
                    label=f"A.{next(steps_a)} upload yaml\ntemplates,"
                    "\nmodel_repo.zip,\nexperiments_lambdas.zip\nto s3"
                )
                >> artifacts_bucket
            )

            deploy_stage = Blank(
                label=f"A.{next(steps_a)} Deploy stage",
                labelloc="",
                height="0.5",
                width="0.95",
            )
            parallel_actions_1 = Blank(
                label=f"A.{next(steps_a)} parallel\nactions",
                labelloc="",
                height="0.5",
                width="0.95",
            )
            parallel_actions_2 = Blank(
                label=f"A.{next(steps_a)} parallel\nactions",
                labelloc="",
                height="0.5",
                width="0.95",
            )

            pipeline - deploy_stage - [parallel_actions_1, parallel_actions_2]

            (
                parallel_actions_1
                >> deploy_infra
                >> Edge(label="deploy")
                >> deploy_infra_stack
            )

            (
                parallel_actions_1
                >> deploy_stackset_admin_role
                >> Edge(label="deploy")
                >> deploy_stackset_admin_role_stack
            )

            (
                parallel_actions_1
                >> deploy_stackset_execution_role
                >> Edge(label="deploy")
                >> stackset_execution_role_stack
            )

            (
                parallel_actions_2
                >> deploy_sm_tag_lambda
                >> Edge(label="deploy")
                >> sm_tag_lambda_stack
            )

            (
                parallel_actions_2
                >> deploy_sc_supervised_learning_project
                >> Edge(label="deploy")
                >> sc_project_stack
            )

            build_aws_codeartifact_stage = Blank(
                label=f"A.{next(steps_a)} Build_AWS_CodeArtifact\nstage",
                labelloc="",
                height="0.5",
                width="0.95",
            )
            pipeline - build_aws_codeartifact_stage

            build_aws_codeartifact_stage >> build_codeartifact_project

            (
                build_codeartifact_project
                >> Edge(label=f"A.{next(steps_a)} upload python\nlibraries")
                >> codeartifact
            )

        (
            deploy_infra_stack
            >> Edge(label="create repo.", style="dashed")
            >> codeartifact
        )

        return


def make_use_case_b(
    fn="images/component_reference/B_create_sagemaker_project.png",
):
    """Use-case B: As a Data Science Admin (DataScienceAdmin role), create a
    SageMaker Project.

    """

    graph_attr = {
        "splines": "polylines"
        # "splines": "spline"
    }

    _filename = os.path.splitext(fn)[0]
    _outformat = os.path.splitext(fn)[1].lstrip(".").lower()

    diagram_kwargs = {
        "name": "",
        "filename": _filename,
        "outformat": _outformat,
        "show": False,
        # "curvestyle": "curved",
        # "curvestyle": "ortho",
        # "curvestyle": "splines",
        "direction": "TB",
        "graph_attr": graph_attr,
    }

    steps_b = count(1)

    with Diagram(**diagram_kwargs):
        role = IAMRole("DataScienceAdmin")
        artifacts_bucket = S3(
            "ArtifactsBucket\n{account_id}-{region}-mlops-artifacts"
        )
        artifacts_bucket_2 = S3(
            "ArtifactsBucket\n{account_id}-{region}-mlops-artifacts"
        )
        # artifacts_bucket_3 = (
        #     S3("ArtifactsBucket\n{account_id}-{region}-mlops-artifacts")
        # )
        sagemaker = Sagemaker("Amazon\nSageMaker")

        project_ready_notification_lambda = LambdaFunction(
            "studio-project-ready-notify\n(use-case A)"
        )

        with Cluster(
            "AWS Management Console",
            graph_attr={
                "fontcolor": "red",
                "pencolor": "red",
                "style": "dashed",
                "bgcolor": "none",
            },
        ):
            sm_domain = Sagemaker("SageMaker\nDomain")
            sm_studio = Sagemaker("SageMaker\nStudio")
            sm_project_catalog = ServiceCatalog(
                "SageMaker\nProject\n(service-catalog-product)"
            )

        # ---

        (
            role
            >> Edge(
                label=f"B.{next(steps_b)} open via aws\nmanagement console",
                style="solid",
            )
            >> sm_domain
        )

        (
            sm_domain
            >> Edge(
                label=f"B.{next(steps_b)} launch\n'SageMaker Project'\napp",
                style="solid",
            )
            >> sm_studio
        )

        (
            role
            >> Edge(label=f"B.{next(steps_b)} create project", style="solid")
            >> sm_studio
        )

        (
            sm_studio
            >> Edge(label=f"B.{next(steps_b)} create project")
            >> sm_project_catalog
        )

        (
            sm_project_catalog
            << Edge(label=f"B.{next(steps_b)} load\n2-smproject_yaml")
            << artifacts_bucket
        )

        mlops_platform_repo = Codecommit(
            "MlopsPlatformRepo\n"
            "aws-enterprise-mlops-platform\n"
            "(use-case A)\n"
            "(codecommit)"
        )

        service_catalog_stack = CloudformationStack(
            "{project_name}-service\n-catalog-stack\n(cfn-stack)"
        )
        ecr_repo_stack = CloudformationStack(
            "{project_name}-ecr\n-repo-stack\n(cfn-stack)"
        )
        model_group_stack = CloudformationStack(
            "{project_name}-model\n-group-stack\n(cfn-stack)"
        )
        inference_stackset_staging_stack = CloudformationStack(
            "{project_name}-inference\n-stackset-staging\n(cfn-stack)"
        )
        inference_stackset_prod_stack = CloudformationStack(
            "{project_name}-inference\n-stackset-prod\n(cfn-stack)"
        )

        with Cluster("SC-{account_id}-pp-*- Stack"):
            project_stack = CloudformationStack(
                "SC-{account_id}-pp-*\n(cfn-stack)"
            )
            project_bucket = S3("ProjectBucket\n{project_name}-{account_id}")
            project_pipeline = Codepipeline(
                "ProjectPipeline\n{project_name}_project_pipeline\n"
                "(codepipeline)"
            )
            project_repo = Codecommit(
                "ProjectCommitRepository\n{project_name}-project-repo\n"
                "(codecommit)"
            )

            build_lcc = Codebuild(
                "LifeCycleConfigProject\nbuild_lcc\n(codebuild-action)"
            )
            build_cfn = Codebuild(
                "BuildCfnProject\nbuild_cfn\n(codebuild-action)"
            )

            (
                sm_project_catalog
                >> Edge(xlabel=f"B.{next(steps_b)} deploy\n2-smproject.yaml")
                >> project_stack
            )

            (
                artifacts_bucket_2
                >> Edge(label=f"B.{next(steps_b)} init w/\nmodel_repo.zip")
                >> project_repo
            )

            (
                project_pipeline
                << Edge(xlabel=f"B.{next(steps_b)} Source stage")
                << mlops_platform_repo
            )

            build_cfn_stage = Blank(
                label=f"B.{next(steps_b)} BuildCFN stage",
                labelloc="",
                height="0.5",
                width="0.95",
            )
            (
                project_pipeline
                - build_cfn_stage
                - Edge(label=f"B.{next(steps_b)} action")
                >> build_lcc
            )
            (
                build_lcc
                >> Edge(label=f"B.{next(steps_b)} upload\nextension.tar.gz")
                >> project_bucket
            )
            (
                build_lcc
                >> Edge(xlabel=f"B.{next(steps_b)} create\nlifecycle config")
                >> sm_studio
            )
            (
                build_cfn_stage
                >> Edge(xlabel=f"B.{next(steps_b)} action")
                >> build_cfn
            )
            (
                build_cfn
                >> Edge(
                    xlabel=f"B.{next(steps_b)} upload\ncustom 3-smuser.yaml"
                )
                >> artifacts_bucket
            )

            # BuildParams stage

            build_params_stage = Blank(
                label=f"B.{next(steps_b)} BuildParams stage",
                labelloc="",
                height="0.5",
                width="0.95",
            )

            # generate params.json file locally
            build_model_groups_params = Codebuild(
                "ModelGroupsParamsProject\nbuild_model_group_params\n"
                "(codebuild-action)"
            )

            (
                project_pipeline
                - build_params_stage
                - Edge(label=f"B.{next(steps_b)} action")
                >> build_model_groups_params
            )

            create_sm_experiment = Codebuild(
                "SMExperimentProject\ncreate_sm_experiment\n(codebuild-action)"
            )

            (
                build_params_stage - Edge(label=f"B.{next(steps_b)} action")
                >> create_sm_experiment
            )

            (
                create_sm_experiment
                >> Edge(label=f"B.{next(steps_b)} create experiment")
                >> sagemaker
            )

            # Dpeloy stage

            deploy_stage = Blank(
                label=f"B.{next(steps_b)} Deploy stage",
                labelloc="",
                height="0.5",
            )

            parallel_actions = Blank(
                label=f"A.{next(steps_b)} parallel\nactions",
                labelloc="",
                height="0.5",
                width="0.95",
            )

            # deploys the user service catalog stack for this project
            deploy_service_catalog = Codebuild(
                "deploy_service_catalog\n(codebuild-action)"
            )

            # deploys the ecr repository for this project
            deploy_ecr = Codebuild("deploy_ecr\n(codebuild-action)")

            # deploys the model package group for this project
            deploy_model_group = Codebuild(
                "deploy_model_group\n(codebuild-action)"
            )

            # staging and prod model deployment stacks
            deploy_model_stackset_stage = Codebuild(
                "deploy_model_stackset_stage\n(codebuild-action)"
            )
            deploy_model_stackset_prod = Codebuild(
                "deploy_model_stackset_prod\n(codebuild-action)"
            )

            project_ready_notification = Codebuild(
                "project_ready_notification\n(codebuild-action)"
            )

            project_pipeline - deploy_stage

            deploy_stage - parallel_actions >> [
                deploy_service_catalog,
                deploy_ecr,
                deploy_model_group,
                deploy_model_stackset_stage,
                deploy_model_stackset_prod,
            ]

            (
                deploy_service_catalog
                >> Edge(label="deploy")
                >> service_catalog_stack
            )

            deploy_ecr >> Edge(label="deploy") >> ecr_repo_stack

            deploy_model_group >> Edge(label="deploy") >> model_group_stack

            (
                deploy_model_stackset_stage
                >> Edge(label="deploy")
                >> inference_stackset_staging_stack
            )

            (
                deploy_model_stackset_prod
                >> Edge(label="deploy")
                >> inference_stackset_prod_stack
            )

            notify_stage = Blank(
                label=f"B.{next(steps_b)} Notify stage",
                labelloc="",
                height="0.5",
            )
            (
                project_pipeline - notify_stage
                >> Edge(label="action")
                >> project_ready_notification
                >> Edge(label=f"B.{next(steps_b)} trigger")
                >> project_ready_notification_lambda
            )


def make_use_case_c(fn="images/component_reference/C_create_user.png"):
    """Use-case C: As a Data Science Admin (DataScienceAdmin role), create a
    user of the project for a data scientist.

    """

    graph_attr = {
        "splines": "polylines"
        # "splines": "spline"
    }

    _filename = os.path.splitext(fn)[0]
    _outformat = os.path.splitext(fn)[1].lstrip(".").lower()

    diagram_kwargs = {
        "name": "",
        "filename": _filename,
        "outformat": _outformat,
        "show": False,
        # "curvestyle": "curved",
        # "curvestyle": "ortho",
        # "curvestyle": "splines",
        "direction": "LR",
        "graph_attr": graph_attr,
    }

    steps_c = count(1)

    with Diagram(**diagram_kwargs):
        role = IAMRole("DataScienceAdmin")

        mlops_platform_repo = Codecommit(
            "MlopsPlatformRepo\n"
            "aws-enterprise-mlops-platform\n"
            "(use-case A)\n"
            "(codecommit)"
        )

        with Cluster(
            "AWS Management Console",
            graph_attr={
                "fontcolor": "red",
                "pencolor": "red",
                "style": "dashed",
                "bgcolor": "none",
            },
        ):
            user_catalog_product = ServiceCatalog(
                "{project_name}\nSageMaker\nStudio User\n"
                "(service-catalog-product)"
            )

            (
                role
                >> Edge(label=f"C.{next(steps_c)} create user")
                >> user_catalog_product
            )

        sm_studio_user = Sagemaker("SageMaker\nStudio\nUser")
        sm_studio_domain = Sagemaker("SageMaker\nStudio\nDomain")

        with Cluster("SC-{account_id}-pp-* Stack"):
            user_stack = CloudformationStack(
                "SageMaker Project\nUser Stack\n"
                "SC-{account_id}-pp-*\n(cfn-stack)"
            )

            pipeline = Codepipeline(
                "UserLCCPipeline\n{project_name}_{user}_pipeline\n"
                "(codepipeline)"
            )

            (
                user_catalog_product
                >> Edge(label=f"C.{next(steps_c)} deploy")
                >> user_stack
            )

            (
                mlops_platform_repo
                >> Edge(xlabel=f"C.{next(steps_c)} source stage")
                >> pipeline
            )

            user_stack >> Edge(label="start\npipeline") >> pipeline

            user_stack >> Edge(label="deploy") >> sm_studio_user

            user_lcc_project = Codebuild(
                "UserLifeCycleConfigProject\n"
                "associate_user_lifecycle\n"
                "(codebuild-action)"
            )

            (
                pipeline
                - Edge(label=f"C.{next(steps_c)} CreateAssociation\nstage")
                >> user_lcc_project
            )

            user_lcc_project - Blank(
                label=f"C.{next(steps_c)} associate\nuser w/ domain",
                labelloc="",
                height="0.5",
            ) - Edge(style="dashed") >> [sm_studio_user, sm_studio_domain]

    return


def make_use_case_d(fn="images/component_reference/D_launch_sm_studio.png"):
    """Use-case D: As a Data Scientist (DataScientist role), use SageMaker
    Studio to start model development.

    """

    graph_attr = {
        "splines": "polylines"
        # "splines": "spline"
    }

    _filename = os.path.splitext(fn)[0]
    _outformat = os.path.splitext(fn)[1].lstrip(".").lower()

    diagram_kwargs = {
        "name": "",
        "filename": _filename,
        "outformat": _outformat,
        "show": False,
        # "curvestyle": "curved",
        # "curvestyle": "ortho",
        # "curvestyle": "splines",
        "direction": "LR",
        "graph_attr": graph_attr,
    }

    steps_d = count(1)

    with Diagram(**diagram_kwargs):
        proj_bucket = S3(
            "ProjectBucket\n{project_name}-{account_id}\n(use-case B)"
        )
        proj_repo = Codecommit(
            "ProjectCommitRepository\n{project_name}-project-repo\n"
            "(use-case B)\n"
            "(codecommit)"
        )
        ds_role = IAMRole("DataScientist")

        with Cluster(
            "AWS Management Console",
            graph_attr={
                "fontcolor": "red",
                "pencolor": "red",
                "style": "dashed",
                "bgcolor": "none",
            },
        ):
            sm_studio = Sagemaker("SageMaker\nStudio")

        sm_processing = Sagemaker("SageMaker\nProcessing")
        sm_training = Sagemaker("SageMaker\nTraining")
        sm_batch_transform = Sagemaker("SageMaker\nBatch Transform")
        sm_endpoint = Sagemaker("SageMaker\nEndpoint")
        sm_hyperparameter_tuning = Sagemaker(
            "SageMaker\nHyperparameter\nTuning"
        )

        # in-order
        (
            ds_role
            >> Edge(label=f"D.{next(steps_d)} open\nSageMaker\nstudio")
            >> sm_studio
        )
        (
            sm_studio
            << Edge(label=f"D.{next(steps_d)} git clone\nmodel code")
            << proj_repo
        )
        (
            sm_studio
            >> Edge(xlabel=f"D.{next(steps_d)} launch\nprocessing job")
            >> sm_processing
        )
        (
            sm_processing
            << Edge(xlabel=f"D.{next(steps_d)} load\nraw CSV(s)")
            << proj_bucket
        )
        (
            sm_processing
            >> Edge(xlabel=f"D.{next(steps_d)} save\ntrain, test, val. CSVs")
            >> proj_bucket
        )
        (
            sm_studio
            >> Edge(label=f"D.{next(steps_d)} launch\ntraining job")
            >> sm_training
        )
        (
            sm_training
            << Edge(label=f"D.{next(steps_d)} load\ntrain, val. CSVs")
            << proj_bucket
        )
        (
            sm_training
            >> Edge(label=f"D.{next(steps_d)} save model")
            >> proj_bucket
        )
        (
            sm_studio
            >> Edge(
                label=f"D.{next(steps_d)} launch\nbatch transform\njob",
                style="curved",
            )
            >> sm_batch_transform
        )
        (
            sm_batch_transform
            << Edge(xlabel=f"D.{next(steps_d)} load\ntest CSV(s)")
            << proj_bucket
        )
        (
            sm_batch_transform
            >> Edge(
                xlabel=f"D.{next(steps_d)} save\nprediction CSV(s)", minlen="3"
            )
            >> proj_bucket
        )

        (
            sm_studio
            >> Edge(xlabel=f"D.{next(steps_d)} deploy\nendpoint")
            >> sm_endpoint
        )

        (
            sm_endpoint
            << Edge(xlabel=f"D.{next(steps_d)} load model")
            << proj_bucket
        )

        (
            sm_studio
            >> Edge(
                label=f"D.{next(steps_d)} launch\nhyperparameter\ntuning job"
            )
            >> sm_hyperparameter_tuning
        )
        (
            sm_hyperparameter_tuning
            << Edge(xlabel=f"D.{next(steps_d)} load model,\ntrain, val CSV(s)")
            << proj_bucket
        )

    return


def make_use_case_e(fn="images/component_reference/E_training.png"):
    """Use-case E: As a Data Scientist (DataScientist role), trigger the model
    building.

    """

    graph_attr = {
        "splines": "polylines"
        # "splines": "spline"
    }

    _filename = os.path.splitext(fn)[0]
    _outformat = os.path.splitext(fn)[1].lstrip(".").lower()

    diagram_kwargs = {
        "name": "",
        "filename": _filename,
        "outformat": _outformat,
        "show": False,
        # "curvestyle": "curved",
        # "curvestyle": "ortho",
        # "curvestyle": "splines",
        "direction": "LR",
        "graph_attr": graph_attr,
    }

    steps_e = count(1)

    with Diagram(**diagram_kwargs):
        role = IAMRole("DataScientist")

        proj_repo = Codecommit(
            "ProjectCommitRepository\n{project_name}-project-repo\n"
            "(use-case B)\n"
            "(codecommit)"
        )

        mlops_platform_repo = Codecommit(
            "MlopsPlatformRepo\n"
            "aws-enterprise-mlops-platform\n"
            "(use-case A)\n"
            "(codecommit)"
        )

        sagemaker = Sagemaker("Amazon\nSageMaker")

        with Cluster(
            "AWS Management Console",
            graph_attr={
                "fontcolor": "red",
                "pencolor": "red",
                "style": "dashed",
                "bgcolor": "none",
            },
        ):
            sm_studio = Sagemaker("SageMaker\nStudio")

            (
                role
                >> Edge(
                    label=f"E.{next(steps_e)} log into\nSageMaker Studio\n"
                    "via AWS Management Console"
                )
                >> sm_studio
            )
            (
                role
                >> Edge(label=f"E.{next(steps_e) } modify\nmodel code")
                >> sm_studio
            )

        (
            sm_studio
            >> Edge(label=f"E.{next(steps_e)} create\npull request")
            >> proj_repo
        )

        (
            role
            >> Edge(label=f"E.{next(steps_e)} merge\n" "pull request\nto main")
            >> proj_repo
        )

        model_build_pipeline = Codepipeline(
            "ModelBuildPipeline\n"
            "{project_name}_build_pipeline\n"
            "(codepipeline)"
        )

        source_stage = Blank(
            label=f"E.{next(steps_e)} Source stage",
            labelloc="",
            height="0.5",
        )

        [proj_repo, mlops_platform_repo] - Edge(style="dashed") - source_stage

        (
            proj_repo
            >> Edge(
                label=f"E.{next(steps_e)} trigger\nmodel build\npipeline",
                style="dashed",
            )
            >> model_build_pipeline
        )

        source_stage >> Edge(style="dashed") >> model_build_pipeline

        push_images_stage = Blank(
            label=f"E.{next(steps_e)} PushImages\nstage",
            labelloc="",
            height="0.5",
        )

        model_build_pipeline - Edge(style="dashed") - push_images_stage

        push_preprocessing = Codebuild(
            "ImageBuildProject\npush_preprocessing\n" "(code-build-action)"
        )
        push_transform = Codebuild(
            "ImageBuildProject\npush_transform\n" "(code-build-action)"
        )
        push_training = Codebuild(
            "ImageBuildProject\npush_training\n" "(code-build-action)"
        )
        push_inference = Codebuild(
            "ImageBuildProject\npush_inference\n" "(code-build-action)"
        )

        (
            push_images_stage
            >> Edge(label=f"E.{next(steps_e)} action", style="dashed")
            >> push_preprocessing
        )

        (
            push_images_stage
            >> Edge(label=f"E.{next(steps_e)} action", style="dashed")
            >> push_transform
        )

        (
            push_images_stage
            >> Edge(label=f"E.{next(steps_e)} action", style="dashed")
            >> push_training
        )

        (
            push_images_stage
            >> Edge(label=f"E.{next(steps_e)} action", style="dashed")
            >> push_inference
        )

        ecr_preprocessing = ECR(
            "{project_name}-repository\n"
            "-preprocessing\n(use-case A)\n(ecr-repository)"
        )
        ecr_transform = ECR(
            "{project_name}-repository\n"
            "-transform\n(use-case A)\n(ecr-repository)"
        )
        ecr_training = ECR(
            "{project_name}-repository\n"
            "-training\n(use-case A)\n(ecr-repository)"
        )
        ecr_inference = ECR(
            "{project_name}-repository\n"
            "-inference\n(use-case A)\n(ecr-repository)"
        )

        (
            push_preprocessing
            >> Edge(label="push container\nimage")
            >> ecr_preprocessing
        )

        push_transform >> Edge(label="push container\nimage") >> ecr_transform

        push_training >> Edge(label="push container\nimage") >> ecr_training

        push_inference >> Edge(label="push container\nimage") >> ecr_inference

        sm_pipeline_stage = Blank(
            label=f"E.{next(steps_e)} SMPipeline\nstage",
            labelloc="",
            height="0.5",
        )

        sm_pipeline = Codebuild(
            "SMPipelineProject\nsm_pipeline\n" "(codebuild-action)"
        )

        (
            model_build_pipeline - sm_pipeline_stage
            >> Edge(label=f"E.{next(steps_e)} action", style="dashed")
            >> sm_pipeline
        )

        (
            sm_pipeline
            >> Edge(
                label=f"E.{next(steps_e)} create/update\n"
                "SageMaker pipeline\nw/ new model"
            )
            >> sagemaker
        )

        proj_bucket = S3("ProjectBucket\n{project_name}-{account_id}")

        (
            sagemaker
            >> Edge(label=f"E.{next(steps_e)} store\nmodel binary")
            >> proj_bucket
        )

        approval = Blank(
            label=f"E.{next(steps_e)} await approval\n" "from use-case F",
            labelloc="",
            height="0.5",
        )

        sagemaker >> Edge(style="dashed") >> approval


def make_use_case_f(fn="images/component_reference/F_approve_deployment.png"):
    """Use-case F: As a Data Scientist (DataScientist role), approve the model
    deployment.

    """

    graph_attr = {
        "splines": "polylines"
        # "splines": "spline"
    }

    _filename = os.path.splitext(fn)[0]
    _outformat = os.path.splitext(fn)[1].lstrip(".").lower()

    diagram_kwargs = {
        "name": "",
        "filename": _filename,
        "outformat": _outformat,
        "show": False,
        # "curvestyle": "curved",
        # "curvestyle": "ortho",
        # "curvestyle": "splines",
        "direction": "LR",
        "graph_attr": graph_attr,
    }

    steps_f = count(1)

    with Diagram(**diagram_kwargs):
        role = IAMRole("DataScientistRole")

        with Cluster(
            "AWS Management Console",
            graph_attr={
                "fontcolor": "red",
                "pencolor": "red",
                "style": "dashed",
                "bgcolor": "none",
            },
        ):
            sm_studio = Sagemaker("SageMaker\nStudio")

        mlops_platform_repo = Codecommit(
            "MlopsPlatformRepo\n"
            "aws-enterprise-mlops-platform\n"
            "(use-case A)\n"
            "(codecommit)"
        )

        (
            role
            >> Edge(
                label=f"F.{next(steps_f)} log into\n"
                "SageMaker Studio\nvia AWS Management Console"
            )
            >> sm_studio
        )

        (
            role
            >> Edge(label=f"F.{next(steps_f)} approve\nlatest model build")
            >> sm_studio
        )

        model_deploy_pipeline = Codepipeline(
            "ModelDeployPipeline\n{project_name}_deploy_pipeline\n"
            "(codepipeline)"
        )

        (
            sm_studio
            >> Edge(
                label=f"F.{next(steps_f)} trigger\npipeline", style="dashed"
            )
            >> model_deploy_pipeline
        )

        source_stage = Blank(
            label=f"F.{next(steps_f)} Source\nstage",
            labelloc="",
            height="0.5",
        )

        (
            mlops_platform_repo
            - Edge(style="dashed")
            - source_stage
            - Edge(style="dashed")
            >> model_deploy_pipeline
        )

        build_model_stage = Blank(
            label=f"F.{next(steps_f)} BuildModel\nstage",
            labelloc="",
            height="0.5",
        )

        model_deploy_pipeline - Edge(style="dashed") - build_model_stage

        build_endpoint_params_staging = Codebuild(
            "EndpointParamsStageProject\n"
            "build_endpoint_params_staging\n(codebuild-action)"
        )

        build_endpoint_params_prod = Codebuild(
            "EndpointParamsProdProject\n"
            "build_endpoint_params_prod\n(codebuild-action)"
        )

        (
            build_model_stage
            >> Edge(label=f"F.{next(steps_f)} action", style="dashed")
            >> build_endpoint_params_staging
        )

        (
            build_model_stage
            >> Edge(label=f"F.{next(steps_f)} action", style="dashed")
            >> build_endpoint_params_prod
        )

        deploy_staging_stage = Blank(
            label=f"F.{next(steps_f)} DeployStaging\nstage",
            labelloc="",
            height="0.5",
        )

        (
            model_deploy_pipeline
            - Edge(label="action", style="dashed")
            - deploy_staging_stage
        )

        deploy_staging = Codebuild("DeployStaging\n(codebuild-action)")

        (
            deploy_staging_stage
            - Edge(label=f"F.{next(steps_f)} action", style="dashed")
            >> deploy_staging
        )

        approve_deployment = Codebuild("ApproveDeployment\n(codebuild-action)")

        (
            deploy_staging_stage
            - Edge(label=f"F.{next(steps_f)} action", style="dashed")
            >> approve_deployment
        )

        with Cluster("{project_name}-inference-stackset-staging StackSet"):
            staging_stack = CloudformationStack(
                "{project_name}-inference\n" "-stackset-staging\n(cfn-stack)"
            )
            deploy_staging >> Edge(label="deploy") >> staging_stack

            (
                role
                >> Edge(
                    label=f"F.{next(steps_f)} manually\napprove deployment",
                    style="dashed",
                )
                >> approve_deployment
            )

            sm_endpoint_staging = Sagemaker("SageMaker\nEndpoint\n(staging)")
            staging_stack >> sm_endpoint_staging

        deploy_prod_stage = Blank(
            label=f"F.{next(steps_f)} DeployProd stage",
            labelloc="",
            height="0.5",
        )

        deploy_prod = Codebuild("DeployProd\n(codebuild-action)")

        with Cluster("{project_name}-inference-stackset-prod StackSet"):
            model_deploy_pipeline - Edge(style="dashed") - deploy_prod_stage

            (
                deploy_prod_stage
                - Edge(label=f"F.{next(steps_f)} action", style="dashed")
                - deploy_prod
            )

            prod_stack = CloudformationStack(
                "{project_name}-inference\n" "-stackset-prod\n(cfn-stack)"
            )

            deploy_prod >> Edge(label="deploy") >> prod_stack

            sm_endpoint_prod = Sagemaker("SageMaker\nEndpoint\n(prod)")
            prod_stack >> sm_endpoint_prod

        proj_bucket = S3(
            "ProjectBucket\n{project_name}-{account_id}\n(use-case B)"
        )

        proj_bucket >> Edge(label="staging\nmodel") >> sm_endpoint_staging
        proj_bucket >> Edge(label="prod\nmodel") >> sm_endpoint_prod

        build_monitor_stage = Blank(
            label=f"F.{next(steps_f)} BuildMonitor stage",
            labelloc="",
            height="0.5",
        )

        build_monitor = Codebuild(
            "BuildMonitor\nbuild_monitor_params\n(codebuild-action)"
        )

        model_deploy_pipeline - Edge(style="dashed") - build_monitor_stage

        (
            build_monitor_stage
            >> Edge(label=f"F.{next(steps_f)} action", style="dashed")
            >> build_monitor
        )

        deploy_monitor_stage = Blank(
            label=f"F.{next(steps_f)} DeployMonitor stage",
            labelloc="",
            height="0.5",
        )

        deploy_monitor = Codebuild(
            "DeployMonitor\nDeployModelMonitor\n(codebuild-action)"
        )

        model_deploy_pipeline - Edge(style="dashed") - deploy_monitor_stage

        (
            deploy_monitor_stage
            >> Edge(label=f"F.{next(steps_f)} action", style="dashed")
            >> deploy_monitor
        )

        with Cluster("{project_name}-monitor-stackset StackSet"):
            monitor_stack = CloudformationStack(
                "{project_name}-monitor\n" "-stackset\n(cfn-stack)"
            )
            sm_monitor = Sagemaker("SageMaker\nModel\nMonitor")

            (
                deploy_monitor - Edge(label="deploy")
                >> monitor_stack
                >> Edge(label="deploy")
                >> sm_monitor
            )

        use_case_g = Blank(
            label="to use-case F",
            labelloc="",
            height="0.5",
        )

        sm_monitor >> Edge(style="dashed") >> use_case_g


def make_use_case_g(fn="images/component_reference/G_monitor_performance.png"):
    """Use-case G: As a Data Scientist (DataScientist role), approve the model
    deployment.

    """

    graph_attr = {
        "splines": "polylines"
        # "splines": "spline"
    }

    _filename = os.path.splitext(fn)[0]
    _outformat = os.path.splitext(fn)[1].lstrip(".").lower()

    diagram_kwargs = {
        "name": "",
        "filename": _filename,
        "outformat": _outformat,
        "show": False,
        # "curvestyle": "curved",
        # "curvestyle": "ortho",
        # "curvestyle": "splines",
        "direction": "LR",
        "graph_attr": graph_attr,
    }

    steps_g = count(1)

    with Diagram(**diagram_kwargs):
        ds_role = IAMRole("DataScientistRole")

        with Cluster(
            "AWS Management Console",
            graph_attr={
                "fontcolor": "red",
                "pencolor": "red",
                "style": "dashed",
                "bgcolor": "none",
            },
        ):
            sm_studio = Sagemaker("SageMaker\nStudio")

        sm_notebook = Sagemaker("SageMaker\nNotebook")
        proj_bucket = S3("ProjectBucket")
        sm_endpoint = Sagemaker("SageMaker\nEndpoint")
        sm_processing = Sagemaker(
            label="SageMaker\nProcessing\n(Monitoring)", margin="20"
        )

        data_quality_task = Blank(
            label="monitor\ndata\nquality", labelloc="c", height="1"
        )
        model_quality_task = Blank(
            label="monitor\nmodel\nquality", labelloc="c", height="1"
        )
        bias_drift_task = Blank(
            label="monitor\nbias\ndrift", labelloc="c", height="1"
        )
        feature_attribution_drift_task = Blank(
            label="monitor\nfeature\nattribution\ndrift",
            labelloc="c",
            height="1",
        )

        (
            ds_role
            >> Edge(label=f"G.{next(steps_g)} open\nSageMaker\nStudio")
            >> sm_studio
        )
        (
            data_quality_task
            >> Edge(label=f"G.{next(steps_g)} open\nSageMaker\nNotebook")
            >> sm_notebook
        )
        (
            sm_studio
            - Edge(label="tbd\nin future\nrelease", style="dotted")
            - [
                model_quality_task,
                bias_drift_task,
                feature_attribution_drift_task,
            ]
        )
        sm_studio - Edge() - data_quality_task

        (
            proj_bucket
            >> Edge(label=f"G.{next(steps_g)} load\ntest CSV(s)")
            >> sm_notebook
        )
        (
            sm_notebook
            >> Edge(
                label=f"G.{next(steps_g)} simulate\nrequest\ntraffic",
                minlen="2",
            )
            >> sm_endpoint
        )
        (
            sm_notebook
            << Edge(
                label=f"G.{next(steps_g)} get\nresponses\n(predictions)",
                minlen="2",
            )
            << sm_endpoint
        )
        (
            sm_endpoint
            >> Edge(label=f"G.{next(steps_g)} capture\nrequests,\nresponses")
            >> proj_bucket
        )

        (
            Blank(
                label="model & data\nquality baseline\nresults\n"
                "(from use-case E)",
                labelloc="c",
            )
            - Edge(headport="n", style="dashed")
            >> proj_bucket
        )
        (
            sm_processing
            << Edge(
                label=f"G.{next(steps_g)} load\ndata & model\n"
                "quality baseline\nresults"
            )
            << proj_bucket
        )
        (
            sm_processing
            >> Edge(
                label=f"G.{next(steps_g)} hourly\nscheduled\ntask",
                headport="w",
                tailport="w",
            )
            >> sm_processing
        )
        (
            sm_processing
            << Edge(
                label=f"G.{next(steps_g)} compare\ncaptured data\n"
                "w/ baseline results"
            )
            << proj_bucket
        )
        (
            sm_processing
            >> Edge(label=f"G.{next(steps_g)} save\nviolations\nreport")
            >> proj_bucket
        )
        (
            sm_notebook
            << Edge(label=f"G.{next(steps_g)} load\nviolations\nreport")
            << proj_bucket
        )

    return


if __name__ == "__main__":
    make_high_level_architecture()
    make_use_case_a()
    make_use_case_b()
    make_use_case_c()
    make_use_case_d()
    make_use_case_e()
    make_use_case_f()
    make_use_case_g()
