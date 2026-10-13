resource "aws_security_group" "alb" {
  name        = "anturi-api-alb"
  description = "alb anturi API security group, allows traffic in port 80, allows traffic out 8000"
  vpc_id      = data.aws_vpc.default_vpc.id

  tags = {
    Name = "anturi-api-alb"
  }
}

resource "aws_vpc_security_group_ingress_rule" "alb_http_in" {
  security_group_id = aws_security_group.alb.id
  ip_protocol       = "tcp"
  from_port         = 80
  to_port           = 80
  cidr_ipv4         = "0.0.0.0/0"
}

resource "aws_vpc_security_group_egress_rule" "alb_to_app" {
  security_group_id            = aws_security_group.alb.id
  ip_protocol                  = "tcp"
  from_port                    = 8000
  to_port                      = 8000
  referenced_security_group_id = aws_security_group.ecs.id
}

resource "aws_security_group" "ecs" {
  name        = "anturi-api-ecs"
  description = "Anturi API ECS tasks: allows inbound 8000 from ALB, all outbound traffic"
  vpc_id      = data.aws_vpc.default_vpc.id
  tags = {
    Name = "anturi-api-ecs"
  }
}

resource "aws_vpc_security_group_ingress_rule" "alb_sends_to_ecs" {
  security_group_id            = aws_security_group.ecs.id
  ip_protocol                  = "tcp"
  from_port                    = 8000
  to_port                      = 8000
  referenced_security_group_id = aws_security_group.alb.id
}

resource "aws_vpc_security_group_egress_rule" "ecs_sends_all" {
  security_group_id = aws_security_group.ecs.id
  ip_protocol       = "-1"
  cidr_ipv4         = "0.0.0.0/0"

}

resource "aws_security_group" "rds" {
  name        = "anturi-api-rds"
  description = "Anturi API RDS: allows inbound 5432 from ECS tasks only, no outbound traffic"
  vpc_id      = data.aws_vpc.default_vpc.id
  tags = {
    Name = "anturi-api-rds"
  }
}

resource "aws_vpc_security_group_ingress_rule" "rds_allow_traffic_from_ecs" {
  security_group_id            = aws_security_group.rds.id
  referenced_security_group_id = aws_security_group.ecs.id
  from_port                    = 5432
  to_port                      = 5432
  ip_protocol                  = "tcp"
}