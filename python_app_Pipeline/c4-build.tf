# aws codebuild - First - python and auth with K8s  ************************************

resource "aws_codebuild_project" "containerAppBuild" {
  badge_enabled  = false
  build_timeout  = 60
  name           = "python_app"



  queued_timeout = 480
  service_role   = aws_iam_role.containerAppBuildProjectRole.arn
  tags = {
    Environment = var.env
  }

  artifacts {
    encryption_disabled = false
    # name                   = "container-app-code-${var.env}"
    # override_artifact_name = false
    packaging = "NONE"
    type      = "CODEPIPELINE"
  }



  environment {
    compute_type                = "BUILD_GENERAL1_SMALL"
    image                       = "aws/codebuild/standard:6.0"
    image_pull_credentials_type = "CODEBUILD"
    privileged_mode             = true
    type                        = "LINUX_CONTAINER"
    environment_variable {
              name  = "IMAGE_REPO_NAME"
              type  = "PLAINTEXT"
              value = "yousefshaban/my-python-app"
    }

    environment_variable {
              name  = "IMAGE_TAG"
              type  = "PLAINTEXT"
              value = "latest"
    }



  }


  logs_config {
    cloudwatch_logs {
      status = "ENABLED"
    }

    s3_logs {
      encryption_disabled = false
      status              = "DISABLED"
    }
  }

# how we can dd more source for aws_codebuild_project

  source {

    buildspec  = "${file("buildspec_python.yml")}"
    git_clone_depth     = 0
    insecure_ssl        = false
    report_build_status = false
  #  type                = "CODEPIPELINE"
    type                = "CODEPIPELINE"
  }
}


#aws codeBuild - Project 2 - Install EFS  *********************************************
# resource "aws_codebuild_project" "containerAppBuild_efs" {
#   badge_enabled  = false
#   build_timeout  = 60
#   name           = "efs-1"

#   queued_timeout = 480
#   service_role   = aws_iam_role.containerAppBuildProjectRole.arn
#   tags = {
#     Environment = var.env
#   }

#   artifacts {
#     encryption_disabled = false
#     packaging = "NONE"
#     type      = "CODEPIPELINE"
#   }
# environment {
#     compute_type                = "BUILD_GENERAL1_SMALL"
#     image                       = "aws/codebuild/standard:6.0"
#     image_pull_credentials_type = "CODEBUILD"
#     privileged_mode             = true
#     type                        = "LINUX_CONTAINER"
#   }

#   logs_config {
#     cloudwatch_logs {
#       status = "ENABLED"
#     }

#     s3_logs {
#       encryption_disabled = false
#       status              = "DISABLED"
#     }
#   }

#   source {
#     # buildspec           = data.template_file.buildspec.rendered
#     buildspec  = "${file("EKS-EFS-CSI-Install/02-efs-install-terraform-manifests/buildspec_efs_1.yml")}"
#     git_clone_depth     = 0
#     insecure_ssl        = false
#     report_build_status = false
#     type                = "CODEPIPELINE"
#   }
# }

# #aws codeBuild - Project 3 - Install EFS  *********************************************
# resource "aws_codebuild_project" "containerAppBuild_efs_static" {
#   badge_enabled  = false
#   build_timeout  = 60
#   name           = "efs-static"

#   queued_timeout = 480
#   service_role   = aws_iam_role.containerAppBuildProjectRole.arn
#   tags = {
#     Environment = var.env
#   }

#   artifacts {
#     encryption_disabled = false
#     packaging = "NONE"
#     type      = "CODEPIPELINE"
#   }
# environment {
#     compute_type                = "BUILD_GENERAL1_SMALL"
#     image                       = "aws/codebuild/standard:6.0"
#     image_pull_credentials_type = "CODEBUILD"
#     privileged_mode             = true
#     type                        = "LINUX_CONTAINER"
#   }

#   logs_config {
#     cloudwatch_logs {
#       status = "ENABLED"
#     }

#     s3_logs {
#       encryption_disabled = false
#       status              = "DISABLED"
#     }
#   }

#   source {
#     # buildspec           = data.template_file.buildspec.rendered
#     buildspec  = "${file("EKS-EFS-Static-Provisioning/buildspec_static.yml")}"
#     git_clone_depth     = 0
#     insecure_ssl        = false
#     report_build_status = false
#     type                = "CODEPIPELINE"
#   }
# }


# containerAppBuild_efs_dynamic Project 4
# resource "aws_codebuild_project" "containerAppBuild_efs_dynamic" {
#   badge_enabled  = false
#   build_timeout  = 60
#   name           = "efs-dynamic"

#   queued_timeout = 480
#   service_role   = aws_iam_role.containerAppBuildProjectRole.arn
#   tags = {
#     Environment = var.env
#   }

#   artifacts {
#     encryption_disabled = false
#     packaging = "NONE"
#     type      = "CODEPIPELINE"
#   }
# environment {
#     compute_type                = "BUILD_GENERAL1_SMALL"
#     image                       = "aws/codebuild/standard:6.0"
#     image_pull_credentials_type = "CODEBUILD"
#     privileged_mode             = true
#     type                        = "LINUX_CONTAINER"
#   }

#   logs_config {
#     cloudwatch_logs {
#       status = "ENABLED"
#     }

#     s3_logs {
#       encryption_disabled = false
#       status              = "DISABLED"
#     }
#   }

#   source {
#     # buildspec           = data.template_file.buildspec.rendered
#     buildspec  = "${file("EKS-EFS-Dynamic-Provisioning/03-efs-dynamic-prov-terraform-manifests/buildspec_dynamic.yml")}"
#     git_clone_depth     = 0
#     insecure_ssl        = false
#     report_build_status = false
#     type                = "CODEPIPELINE"
#   }
# }




#aws codeBuild - Project 3 *********************************************

# resource "aws_codebuild_project" "containerAppBuild" {
#   badge_enabled  = false
#   build_timeout  = 60
#   name           = "container-app-build"
#   #build_spec  = "${file("buildspec1.yml")}"
#   queued_timeout = 480
#   service_role   = aws_iam_role.containerAppBuildProjectRole.arn
#   tags = {
#     Environment = var.env
#   }

#   artifacts {
#     encryption_disabled = false
#     # name                   = "container-app-code-${var.env}"
#     # override_artifact_name = false
#     packaging = "NONE"
#     type      = "CODEPIPELINE"
#   }

#   environment {
#     compute_type                = "BUILD_GENERAL1_SMALL"
#     image                       = "aws/codebuild/standard:5.0"
#     image_pull_credentials_type = "CODEBUILD"
#     privileged_mode             = true
#     type                        = "LINUX_CONTAINER"
#   }

#   logs_config {
#     cloudwatch_logs {
#       status = "ENABLED"
#     }

#     s3_logs {
#       encryption_disabled = false
#       status              = "DISABLED"
#     }
#   }

#   source {
#     # buildspec           = data.template_file.buildspec.rendered
#     git_clone_depth     = 0
#     insecure_ssl        = false
#     report_build_status = false
#     type                = "CODEPIPELINE"
#   }
# }