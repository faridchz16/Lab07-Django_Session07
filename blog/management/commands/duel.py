from django.core.management.base import BaseCommand
from blog.duel.questions import QUESTIONS
from blog.duel import team
from blog.duel import ai_answers


class Command(BaseCommand):
    help = 'Runs the duel between team ORM queries and expected or AI queries'

    def add_arguments(self, parser):
        parser.add_argument('--question', type=str, help='Run a single question (e.g. q4)')
        parser.add_argument('--source', type=str, default='team', choices=['team', 'ai'], help='Source of answers: team or ai')

    def handle(self, *args, **options):
        q_filter = options.get('question')
        source = options.get('source')

        module = ai_answers if source == 'ai' else team
        questions_to_run = [q_filter] if q_filter else sorted(QUESTIONS.keys())

        self.stdout.write(f"Running duel using source: {source.upper()}\n")

        all_correct = True
        for q_key in questions_to_run:
            if q_key not in QUESTIONS:
                self.stdout.write(self.style.ERROR(f"Question {q_key} not found."))
                continue

            expected_func = QUESTIONS[q_key]["func"]
            try:
                expected_qs = expected_func()
                expected_sql = str(expected_qs.query)
                expected_eval = list(expected_qs)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"{q_key}: Error in expected query: {e}"))
                continue

            candidate_func = getattr(module, q_key, None)
            if not candidate_func:
                self.stdout.write(self.style.ERROR(f"{q_key}: Function not implemented in {source}."))
                all_correct = False
                continue

            try:
                candidate_qs = candidate_func()
                candidate_sql = str(candidate_qs.query)
                candidate_eval = list(candidate_qs)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"{q_key}: [ERROR] Exception raised: {e}"))
                all_correct = False
                continue

            # Compare results
            is_match = (expected_eval == candidate_eval)
            if is_match:
                self.stdout.write(self.style.SUCCESS(f"{q_key}: CORRECT (SQL: {candidate_sql})"))
            else:
                self.stdout.write(self.style.WARNING(f"{q_key}: DISTINCT RESULT (Expected count: {len(expected_eval)}, Got count: {len(candidate_eval)})"))
                self.stdout.write(f"  Candidate SQL: {candidate_sql}")
                all_correct = False

        if all_correct:
            self.stdout.write(self.style.SUCCESS("\nAll evaluated questions are correct!"))
        else:
            self.stdout.write(self.style.WARNING("\nSome questions differed or failed."))
