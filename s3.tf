data "archive_file" "source_code" {
  type        = "zip"
  source_dir  = var.source_code_path
  output_path = var.source_code_zip
}

data "archive_file" "getter_source_code" {
  type        = "zip"
  source_dir  = var.getter_source_code_path
  output_path = var.getter_source_code_zip
}

resource "aws_s3_bucket" "s3_bucket" {
  bucket = "tf-rpitracker-bucket"
  tags = {
    Name        = "RasPi Tracker Bucket"
    Environment = "Prod"
  }
}

resource "aws_s3_bucket_acl" "bucket_acl" {
  bucket = aws_s3_bucket.s3_bucket.id
  acl    = "private"
}

resource "aws_s3_bucket_public_access_block" "public_access_block_s3" {
  bucket                  = aws_s3_bucket.s3_bucket.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_object" "source_code_in_bucket" {
  bucket = aws_s3_bucket.s3_bucket.id
  key    = "tf_rpitracker.zip"
  source = var.source_code_zip
  etag   = filemd5(var.source_code_zip)
  depends_on = [
    data.archive_file.source_code
  ]
}

resource "aws_s3_object" "getter_source_code_in_bucket" {
  bucket = aws_s3_bucket.s3_bucket.id
  key    = "tf_getter.zip"
  source = var.getter_source_code_zip
  etag   = filemd5(var.getter_source_code_zip)
  depends_on = [
    data.archive_file.getter_source_code
  ]
}

resource "aws_s3_object" "lambda_layer_in_bucket" {
  bucket = aws_s3_bucket.s3_bucket.id
  key    = "tf_rpitrackerLayers.zip"
  source = var.layer_path
}