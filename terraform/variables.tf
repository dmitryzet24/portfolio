variable = "aws_region" {
        description = "Deployment region"
        type = string
        default = "us-east-1"
}

variable "project_name" {
        description = "Project Name"
        type  = string
        default  = "gstore-ltv-project"
}

#variable "vpc_cidr" {
#  description = "MWAA & Redshift Network"
#  type        = string
#  default     = "10.0.0.0/16"
#}
#
variable "environment" {
        description = "Environment"
        type  = string
        defaut = "dev"
}

variable "dredshift_password" {
        description  = "Password for Redshift Serverless"
        type = string
        sensitive  = true

}