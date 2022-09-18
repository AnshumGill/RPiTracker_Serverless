variable "aws_acc_key" {
  type        = string
  description = "Access Key for AWS IAM Role"
}
variable "aws_secret" {
  type        = string
  description = "Secret for AWS IAM Role"
}
variable "source_code_path" {
  type        = string
  description = "Path for Source code"
  default     = "layers/rpitracker"
}
variable "source_code_zip" {
  type        = string
  description = "Filename for Source Code zip file"
  default     = "layers/rpitracker.zip"
}
variable "layer_path" {
  type        = string
  description = "Path for Lamda Layer"
  default     = "layers/modules/rpiTrackerLayer.zip"
}
variable "url_js_path" {
  type        = string
  description = "Path for URL.js file"
  default     = "UI/static/url.js"
}