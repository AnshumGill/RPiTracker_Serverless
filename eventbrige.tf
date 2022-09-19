resource "aws_cloudwatch_event_rule" "cronjob" {
  name                = "tf_rpiTracker_cron"
  schedule_expression = "rate(15 minutes)"
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  arn  = aws_lambda_function.lambda_scraper_function.arn
  rule = aws_cloudwatch_event_rule.cronjob.name
}