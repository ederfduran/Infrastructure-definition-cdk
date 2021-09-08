from aws_cdk import (
    aws_ec2 as ec2,
    aws_ssm as ssm,
    core
)

class VPCStack(core.Stack):
    def __init__(self, scope: core.Construct, id:str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        prj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")

        self.vpc = ec2.Vpc(self, 'devVPC', 
                            cidr="172.32.0.0/16", 
                            # will end up with total_subnets = subnets * 2
                            # (2 public, 2 private and 2 isolated)
                            max_azs=2,
                            # assign public dns for public subnets
                            enable_dns_hostnames=True,
                            enable_dns_support=True,
                            subnet_configuration=[
                                ec2.SubnetConfiguration(
                                    name="Public",
                                    subnet_type=ec2.SubnetType.PUBLIC,
                                    cidr_mask=24
                                ),
                                ec2.SubnetConfiguration(
                                    name="Private",
                                    subnet_type=ec2.SubnetType.PRIVATE,
                                    cidr_mask=24
                                ),
                                ec2.SubnetConfiguration(
                                    name="Isolated",
                                    subnet_type=ec2.SubnetType.ISOLATED,
                                    cidr_mask=24
                                )
                            ],
                            nat_gateways=1)

        private_subnets = [subnet.subnet_id for subnet in self.vpc.private_subnets]
        count = 1 
        for ps in private_subnets:
            ssm.StringParameter(self, 
                                f'private-subnet-{str(count)}',
                                string_value=ps,
                                parameter_name= f'/{env_name}/private-subnet-{str(count)}')
            count += 1