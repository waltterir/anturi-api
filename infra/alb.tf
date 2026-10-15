resource "aws_lb" "anturi_api_alb_lb" {
  name               = "anturi-api-alb"
  load_balancer_type = "application"
  internal           = false
  security_groups    = [aws_security_group.alb.id]
  subnets            = data.aws_subnets.default_subnets.ids
}

resource "aws_lb_target_group" "anturi_api_aws_lb_target_group" {
  name        = "anturi-api-lb-group"
  port        = 8000
  protocol    = "HTTP"
  vpc_id      = data.aws_vpc.default_vpc.id
  target_type = "ip"

  health_check {
    path    = "/health"
    matcher = "200"
  }
}

resource "aws_lb_listener" "anturi_api_lb_listener" {
  load_balancer_arn = aws_lb.anturi_api_alb_lb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.anturi_api_aws_lb_target_group.arn
  }
}
