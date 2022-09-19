resource "aws_dynamodb_table" "table" {
  name           = "tf_rpiTracker"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "model"
  attribute {
    name = "model"
    type = "S"
  }
}