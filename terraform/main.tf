provider "aws" {
  region = var.aws_region
}
# Data Lake
resource "aws_s3_bucket" "data_lake" {
  bucket = "${var.project_name}-${var.environment}-datalake"
}

# Airflow Bucket (DAGs & requirements.txt)
resource "aws_s3_bucket" "mwaa_bucket" {
  bucket = "${var.project_name}-${var.environment}-mwaa-assets"
}

# Datalake structure
resource "aws_s3_object" "data_folders" {
  for_each = toset(["raw/", "staging/", "marts/"])
  bucket   = aws_s3_bucket.data_lake.id
  key      = each.value
}