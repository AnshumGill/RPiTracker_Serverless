resource "aws_lambda_layer_version" "lambda_layer" {
  s3_bucket           = aws_s3_bucket.s3_bucket.id
  s3_key              = aws_s3_object.lambda_layer_in_bucket.key
  s3_object_version   = aws_s3_object.lambda_layer_in_bucket.version_id
  layer_name          = "tf_rpitrackerLayer"
  description         = "httpx and beautifulsoup4 python modules as layer"
  compatible_runtimes = ["python3.8", "python3.9"]
}

resource "aws_lambda_function" "lambda_scraper_function" {
  s3_bucket         = aws_s3_bucket.s3_bucket.id
  s3_key            = aws_s3_object.source_code_in_bucket.key
  s3_object_version = aws_s3_object.source_code_in_bucket.version_id
  function_name     = "tf_rpiTracker"
  role              = aws_iam_role.lambda_role.arn
  handler           = "lambda_function.lambda_handler"
  runtime           = "python3.9"
  layers            = [aws_lambda_layer_version.lambda_layer.arn]
  timeout           = 120
  memory_size       = 512
  source_code_hash  = data.archive_file.source_code.output_base64sha256
}

resource "aws_lambda_function" "lambda_getter_function" {
  s3_bucket         = aws_s3_bucket.s3_bucket.id
  s3_key            = aws_s3_object.getter_source_code_in_bucket.key
  s3_object_version = aws_s3_object.getter_source_code_in_bucket.version_id
  function_name     = "tf_rpiGetter"
  role              = aws_iam_role.lambda_role.arn
  handler           = "lambda_function.lambda_handler"
  runtime           = "python3.9"
  timeout           = 5
  source_code_hash  = data.archive_file.getter_source_code.output_base64sha256
}

resource "aws_lambda_permission" "api_gateway_lambda" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_getter_function.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.rest_api.execution_arn}/*/*/*"
}

resource "aws_lambda_permission" "eventbridge_lambda" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_scraper_function.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.cronjob.arn
}