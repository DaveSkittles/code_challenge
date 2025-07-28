from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from claims.models import Claim, Annotation
from decimal import Decimal
import random
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Populate database with sample medical claims data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--claims',
            type=int,
            default=50,
            help='Number of claims to create (default: 50)'
        )

    def handle(self, *args, **options):
        # Create admin user if doesn't exist
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Created admin user: admin / admin123')
            )

        # Create additional test users
        analyst_user, created = User.objects.get_or_create(
            username='analyst',
            defaults={
                'email': 'analyst@example.com',
                'first_name': 'Claims',
                'last_name': 'Analyst',
            }
        )
        if created:
            analyst_user.set_password('analyst123')
            analyst_user.save()

        # Sample data for realistic claims
        patient_names = [
            'John Smith', 'Jane Doe', 'Michael Johnson', 'Sarah Williams', 'David Brown',
            'Emily Davis', 'Robert Miller', 'Lisa Wilson', 'William Moore', 'Jennifer Taylor',
            'James Anderson', 'Mary Thomas', 'Christopher Jackson', 'Patricia White', 'Daniel Harris',
            'Barbara Martin', 'Matthew Thompson', 'Nancy Garcia', 'Anthony Martinez', 'Dorothy Robinson',
        ]

        insurers = [
            'Blue Cross Blue Shield', 'Aetna', 'Cigna', 'UnitedHealthcare', 'Humana',
            'Kaiser Permanente', 'Anthem', 'Tricare', 'Medicare', 'Medicaid'
        ]

        providers = [
            'General Hospital', 'City Medical Center', 'Regional Healthcare', 'Community Clinic',
            'Specialty Care Associates', 'Primary Care Partners', 'Emergency Medical Services',
            'Urgent Care Plus', 'Wellness Center', 'Family Medicine Group'
        ]

        # Common CPT codes (medical procedures)
        cpt_codes = [
            '99213', '99214', '99215', '99242', '99243', '99244', '99245',
            '73721', '73722', '73723', '70450', '70460', '70470',
            '93000', '93005', '93010', '80053', '80061', '85025',
            '36415', '90471', '90472', '90715', '90736'
        ]

        # Common ICD-10 diagnosis codes
        diagnosis_codes = [
            'M79.89', 'Z00.00', 'I10', 'E11.9', 'M25.50', 'J06.9',
            'R50.9', 'Z01.419', 'M54.2', 'K21.9', 'F41.1', 'N39.0',
            'J20.9', 'R06.02', 'M62.838', 'G43.909', 'K59.00', 'R53.83'
        ]

        denial_reasons = [
            'Prior authorization required but not obtained',
            'Procedure not covered under current plan',
            'Claim submitted after filing deadline',
            'Insufficient documentation provided',
            'Service not medically necessary',
            'Duplicate claim submission',
            'Provider not in network',
            'Coordination of benefits required',
            'Pre-existing condition exclusion',
            'Annual benefit limit exceeded'
        ]

        sample_annotations = [
            'Reviewed medical records - underpayment confirmed',
            'Prior authorization was obtained, claim should be reprocessed',
            'Provider documentation supports medical necessity',
            'Similar claims from this provider show pattern of underpayment',
            'Patient has secondary insurance that should cover difference',
            'CPT code appears to be incorrectly denied',
            'Claim meets all policy requirements for full payment',
            'Coordination of benefits may resolve payment discrepancy',
            'Provider contract terms support higher reimbursement',
            'Medical review indicates appropriate level of service'
        ]

        # Clear existing data
        Claim.objects.all().delete()
        Annotation.objects.all().delete()

        claims_to_create = options['claims']
        self.stdout.write(f'Creating {claims_to_create} sample claims...')

        for i in range(claims_to_create):
            # Generate realistic financial amounts
            billed_amount = Decimal(random.randint(100, 5000))
            
            # Create different scenarios based on status
            status = random.choices(
                ['approved', 'denied', 'underpaid', 'pending'],
                weights=[40, 20, 30, 10]
            )[0]
            
            if status == 'approved':
                paid_amount = billed_amount
            elif status == 'denied':
                paid_amount = Decimal('0.00')
            elif status == 'underpaid':
                # Underpaid by 20-80% of billed amount
                underpaid_factor = random.uniform(0.2, 0.8)
                paid_amount = billed_amount * Decimal(str(1 - underpaid_factor))
            else:  # pending
                paid_amount = Decimal('0.00')

            # Service date within last year
            service_date = date.today() - timedelta(days=random.randint(1, 365))

            claim = Claim.objects.create(
                claim_id=f'CLM{2024}{str(i+1).zfill(6)}',
                patient_name=random.choice(patient_names),
                billed_amount=billed_amount,
                paid_amount=paid_amount.quantize(Decimal('0.01')),
                status=status,
                insurer_name=random.choice(insurers),
                denial_reason=random.choice(denial_reasons) if status == 'denied' else None,
                cpt_codes=random.sample(cpt_codes, random.randint(1, 3)),
                diagnosis_codes=random.sample(diagnosis_codes, random.randint(1, 2)),
                service_date=service_date,
                provider_name=random.choice(providers),
                flagged_for_review=random.choice([True, False]) if random.random() < 0.3 else False
            )

            # Add some annotations to random claims
            if random.random() < 0.4:  # 40% of claims get annotations
                num_annotations = random.randint(1, 2)
                for _ in range(num_annotations):
                    Annotation.objects.create(
                        claim=claim,
                        user=random.choice([admin_user, analyst_user]),
                        content=random.choice(sample_annotations)
                    )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {claims_to_create} claims with sample data')
        )
        self.stdout.write(
            self.style.SUCCESS('Login credentials:')
        )
        self.stdout.write('  Admin: admin / admin123')
        self.stdout.write('  Analyst: analyst / analyst123') 