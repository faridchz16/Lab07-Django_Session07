import json
from django.core.management.base import BaseCommand
from blog.agent.registry import execute_intent


class Command(BaseCommand):
    help = 'Executes an agent intent against the closed registry sandbox'

    def add_arguments(self, parser):
        parser.add_argument('--intent', type=str, required=True, help='JSON string representing intent')
        parser.add_argument('--approve', action='store_true', help='Approve destructive action')
        parser.add_argument('--hash', type=str, default=None, help='Plan hash for verification')

    def handle(self, *args, **options):
        intent_str = options.get('intent')
        approve = options.get('approve')
        plan_hash = options.get('hash')

        try:
            intent_dict = json.loads(intent_str)
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f"Invalid JSON intent: {e}"))
            return

        result = execute_intent(intent_dict, approved=approve, plan_hash=plan_hash)
        self.stdout.write(json.dumps(result, indent=2))
        
        status = result.get("status")
        if status == "ok":
            self.stdout.write(self.style.SUCCESS("\nIntent executed successfully."))
        elif status == "approval_required":
            self.stdout.write(self.style.WARNING("\nApproval required for destructive action."))
        else:
            self.stdout.write(self.style.ERROR(f"\nIntent status: {status}"))
