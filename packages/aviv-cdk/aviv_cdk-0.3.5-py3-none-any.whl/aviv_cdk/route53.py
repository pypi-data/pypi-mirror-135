import typing
from constructs import Construct
from aws_cdk import (
    CfnOutput,
    aws_route53,
    aws_certificatemanager
)


class HostedZone(Construct):
    zone: aws_route53.IHostedZone
    fqdn: str

    def __init__(self, scope: Construct, id: str, *, fqdn: str,  zone_id: str=None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.fqdn = fqdn
        if zone_id:
            self.zone = aws_route53.HostedZone.from_hosted_zone_attributes(self, 'zone', hosted_zone_id=zone_id, zone_name=fqdn)
        else:
            self.zone = aws_route53.HostedZone(self, 'zone', zone_name=fqdn)

    def TxtRecord(self, record_name: str, values: list):
        return aws_route53.TxtRecord(
            self, record_name + '-txt',
            record_name=record_name,
            zone=self.zone,
            values=values
        )

    def CnameRecord(self, record_name: str, domain_name: str) -> aws_route53.CnameRecord:
        return aws_route53.CnameRecord(
            self, record_name + '-cname',
            domain_name=domain_name,
            zone=self.zone,
            record_name=record_name
        )

    def ARecord(self, record_name: str, target: typing.Union[aws_route53.RecordTarget, list]) -> aws_route53.ARecord:
        return aws_route53.ARecord(
            self, record_name + '-a',
            target=target,
            zone=self.zone,
            record_name=record_name
        )

    def ZoneDelegationRecord(self, record_name: str, name_servers: list) -> aws_route53.ZoneDelegationRecord:
        return aws_route53.ZoneDelegationRecord(
            self, record_name + '-ns',
            name_servers=name_servers,
            zone=self.zone,
            record_name=record_name
        )

    def create_certificate(self, domain_name: str, subject_alternative_names: list=None, cert_authority: str=None):
        domid = domain_name.replace('.', '')
        self.cert = aws_certificatemanager.Certificate(
            self, f"{domid}-certificate",
            domain_name=domain_name,
            subject_alternative_names=subject_alternative_names,
            validation=aws_certificatemanager.CertificateValidation.from_dns(hosted_zone=self.zone)
        )
        CfnOutput(self, f"{domid}-certificate-arn", value=self.cert.certificate_arn, export_name=f"{domid}-cert-arn")
        return self.cert
