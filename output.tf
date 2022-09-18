resource "local_file" "invoke_url_dump" {
  filename = var.url_js_path
  content  = "var api_gateway_url = \"${aws_api_gateway_stage.api_gateway_stage.invoke_url}\";"
}