resourse "aws_iam_role" "redshift_s3_role" {
  name = "store_redshift_s3_access"

  assume_role_policy = jsondecode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "redshif.amazonaws.com"
        }
      },
    ]
  })
}

# Read-only from S3
resource "aws_iam_role_policy" "s3_read_policy" {
  name = "s3_read_policy"
  role = aws_iam_role.redshift_s3_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = ["s3.Get*", "s3.List*"]
        Effect = "Allow"
        Resource = ["${aws_s3_bucket.datalake.arn}", "${aws_s3_bucket.datalake.arn}/*"]
      }
    ]
  })
}

