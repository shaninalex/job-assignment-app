import pika
from pika.adapters.blocking_connection import BlockingChannel

from database import Candidate, CompanyManager, Company, Auth


def create_new_candidate(channel: BlockingChannel, candidate: Candidate):
    d = {"candidate": candidate.json()}
    channel.basic_publish(
        'ex.admin_events',
        'candidate',
        str(d),
        pika.BasicProperties(
            content_type='text/json',
            delivery_mode=pika.DeliveryMode.Transient)
    )

def confirm_account(channel: BlockingChannel, auth: Auth, name: str):
    d = {
        "name": name,
        "email": auth.email,
        "code": "TODO: generate code"
    }
    channel.basic_publish(
        'ex.email',
        'candidate',
        str(d),
        pika.BasicProperties(
            content_type='text/json',
            delivery_mode=pika.DeliveryMode.Transient)
    )

def create_new_company(channel: BlockingChannel, company: Company, member: CompanyManager):
    d = {
        "company": company.json(),
        "member": member.json(),
    }
    channel.basic_publish(
        'ex.admin_events',
        'candidate',
        str(d),
        pika.BasicProperties(
            content_type='text/json',
            delivery_mode=pika.DeliveryMode.Transient)
    )