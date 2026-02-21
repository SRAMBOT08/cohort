"""
Management command to create all students with mentor assignments
Data is hardcoded from package-lock.xlsx (mentor wise sheet)
Runs automatically during Render build
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

# Student data: (username, email, first_name, second_name, mentor_name)
STUDENTS_DATA = [
    ('ABINA J', 'abina.j.it.2024@snsct.org', '', '', 'GOPI KRISHNAN'),
    ('ADITHYEN K', 'adithyen.k.cse.2024@snsce.ac.in', '', '', 'GOPI KRISHNAN'),
    ('AKILESH M P', 'akilesh.mp.it.2024@snsct.org', '', '', 'GOPI KRISHNAN'),
    ('AMAL KRISHNA A S', 'amala.s.cst.2024@snsce.ac.in', '', '', 'GOPI KRISHNAN'),
    ('AMAL RAAJAN S', 'amalraajan.s.csd.2024@snsce.ac.in', '', '', 'GOPI KRISHNAN'),
    ('ANISHA M', 'anisha.m.csd.2024@snsce.ac.in', '', '', 'GOPI KRISHNAN'),
    ('ANTONY RAJ V', 'antraj.v.it.2024@snsce.ac.in', '', '', 'GOPI KRISHNAN'),
    ('ARATHI SURESH', 'arathi.s.cst.2024@snsce.ac.in', '', '', 'GOPI KRISHNAN'),
    ('ARUNPANDIYAN', 'arun.s.cse.2024@snsce.ac.in', '', '', 'GOPI KRISHNAN'),
    ('CHAKRATHARIE V', 'chakratharie.v.aiml.2024@snsct.org', '', '', 'GOPI KRISHNAN'),
    ('CIBIVISHNU', 'cibivishnu.p.csd.2024@snsce.ac.in', '', '', 'GOPI KRISHNAN'),
    ('DIVAGAR J M', 'divagr.jm.ad.2024@snsce.ac.in', '', '', 'GOPI KRISHNAN'),
    ('GANESHKUMAR P', 'ganeshkumar.p.csd.2024@snsce.ac.in', '', '', 'GOPI KRISHNAN'),
    ('GNANASRI C', 'gnanasri.c.cse.2024@snsce.ac.in', '', '', 'GOPI KRISHNAN'),
    ('GOBINATH G', 'gobinath.g.csd.2024@snsce.ac.in', '', '', 'GOPI KRISHNAN'),
    ('GOPIKA SREE K C', 'gopika.kc.cse.2024@snsce.ac.in', '', '', 'GOPI KRISHNAN'),
    ('GOPINATH V', 'gopi.v.iot.2024@snsce.ac.in', '', '', 'GOPI KRISHNAN'),
    ('KAVIN A', 'kavin.a.it.2024@snsce.ac.in', '', '', 'GOPI KRISHNAN'),
    ('KEERTHANA K', 'keerthana.k.aiml.2024@snsct.org', '', '', 'GOPI KRISHNAN'),
    ('KEERTHANA S', 'keerthana.s.it.2024@snsct.org', '', '', 'GOPI KRISHNAN'),
    ('KISHORE B', 'kishore.b.cst.2024@snsce.ac.in', '', '', 'GOPI KRISHNAN'),
    ('KISHORE E S', 'kishore.es.aiml.2024@snsct.org', '', '', 'GOPI KRISHNAN'),
    ('KRITHIKA V', 'krithika.v.aiml.2024@snsct.org', '', '', 'GOPI KRISHNAN'),
    ('LOKESH KUMAR', 'lokeshkumar.ms.cse.2024@snsct.org', '', '', 'GOPI KRISHNAN'),
    ('LOKESH SUNDAR M M', 'lokeshsundar.mm.aiml.2024@snsct.org', '', '', 'GOPI KRISHNAN'),
    ('MADELINE PRATHANA V', 'madeline.v.cse.2024@snsct.org', '', '', 'GOPI KRISHNAN'),
    ('MARLENE SARANYA S', 'marlenesaranya.s.cse.2024@snsct.org', '', '', 'GOPI KRISHNAN'),
    ('MIRULA A', 'mirula.a.aiml.2024@snsct.org', '', '', 'GOPI KRISHNAN'),
    ('NISHA', 'nisha.p.it.2024@snsct.org', '', '', 'GOPI KRISHNAN'),
    ('NITHARSHINI S G', 'nitharshini.sg.aiml.2024@snsct.org', '', '', 'GOPI KRISHNAN'),
    ('NITHISH R', 'nithis.r.ad.2024@snsce.ac.in', '', '', 'GOPI KRISHNAN'),
    ('POOJA S', 'pooja.s.ad.2024@snsce.ac.in', '', '', 'GOPI KRISHNAN'),
    ('POOJA V R', 'pooja.vr.csd.2024@snsce.ac.in', '', '', 'GOPI KRISHNAN'),
    ('PRANETHI RAMESH', 'pranethi.r.iot.2024@snsce.ac.in', '', '', 'GOPI KRISHNAN'),
    ('PRATHIBA M', 'prathiba.m.it.2024@snsct.org', '', '', 'GOPI KRISHNAN'),
    ('PRIYA DHARSHINI K', 'priya.k.iot.2024@snsce.ac.in', '', '', 'GOPI KRISHNAN'),
    ('PRIYANKA B', 'priyan.b.ad.2024@snsce.ac.in', '', '', 'GOPI KRISHNAN'),
    ('PUGAZHENTHI S', 'pugaz.s.iot.2024@snsce.ac.in', '', '', 'GOPI KRISHNAN'),
    ('RAHUL R', 'rahul.r.ad.2024@snsce.ac.in', '', '', 'GOPI KRISHNAN'),
    ('REMIGIOUS PAUL ANTONY H', 'remipl.h.it.2024@snsce.ac.in', '', '', 'GOPI KRISHNAN'),
    ('SAI SRI N', 'saisri.n.cst.2024@snsce.ac.in', '', '', 'GOPI KRISHNAN'),
    ('SAKTHI S K', 'sakthi.sk.aiml.2024@snsct.org', '', '', 'GOPI KRISHNAN'),
    ('SANDHYA R J', 'sandhya.rj.cse.2024@snsce.ac.in', '', '', 'GOPI KRISHNAN'),
    ('SASMITHA R', 'sasmi.r.ad.2024@snsce.ac.in', '', '', 'GOPI KRISHNAN'),
    ('SIVAPRASATH C', 'sivap.c.it.2024@snsce.ac.in', '', '', 'GOPI KRISHNAN'),
    ('SRINILA G K', 'srinila.gk.csd.2024@snsce.ac.in', '', '', 'GOPI KRISHNAN'),
    ('SRIRAM R P', 'sriram.rp.cse.2024@snsct.org', '', '', 'GOPI KRISHNAN'),
    ('SWETHA S', 'swetha.s.ad.2024@snsce.ac.in', '', '', 'GOPI KRISHNAN'),
    ('THARUN G', 'tharun.g.cse.2024@snsct.org', '', '', 'GOPI KRISHNAN'),
    ('VISHAL V', 'vishal.v.it.2024@snsct.org', '', '', 'GOPI KRISHNAN'),
    ('AFREENA S', 'afreena.s.it.2024@snsct.org', '', '', 'RESHMA RAJ'),
    ('ARAVINTH P', 'aravinth.p.aiml.2024@snsct.org', '', '', 'RESHMA RAJ'),
    ('BALAPRAPAKARAN K', 'balaprapakaran.k.aiml.2024@snsct.org', '', '', 'RESHMA RAJ'),
    ('BALASURYA', 'bsurya.n.it.2024@snsce.ac.in', '', '', 'RESHMA RAJ'),
    ('BAVISH', 'bavish.ma.aiml.2024@snsct.org', '', '', 'RESHMA RAJ'),
    ('BHARANIDHARAN S', 'bharan.s.ad.2024@snsce.ac.in', '', '', 'RESHMA RAJ'),
    ('BHAVATARINI S', 'bhavatarini.s.aiml.2024@snsct.org', '', '', 'RESHMA RAJ'),
    ('BHAVYASRI J', 'bhavyasri.j.iot.2024@snsce.ac.in', '', '', 'RESHMA RAJ'),
    ('BHUSHAN V', 'bhushan.v.cse.2024@snsce.ac.in', '', '', 'RESHMA RAJ'),
    ('CHANDRU S', 'chandru.s.cse.2024@snsce.ac.in', '', '', 'RESHMA RAJ'),
    ('DEEKSHITHAA R S', 'deekshi.rs.cse.2024@snsce.ac.in', '', '', 'RESHMA RAJ'),
    ('DHANUSHRI V L', 'dhanu.vl.ad.2024@snsce.ac.in', '', '', 'RESHMA RAJ'),
    ('DHARUNYA SRI S', 'dharun.s.ad.2024@snsce.ac.in', '', '', 'RESHMA RAJ'),
    ('DINESH S', 'dinesh.s.ad.2024@snsce.ac.in', '', '', 'RESHMA RAJ'),
    ('GIRIDHARAN R', 'giri.r.cst.2024@snsce.ac.in', '', '', 'RESHMA RAJ'),
    ('GOKUL KANNA P', 'gokulkanna.p.it.2024@snsct.org', '', '', 'RESHMA RAJ'),
    ('GOKUL R', 'gokul.r.aiml.2024@snsct.org', '', '', 'RESHMA RAJ'),
    ('GOWRI SANJAI V', 'gowri.v.it.2024@snsce.ac.in', '', '', 'RESHMA RAJ'),
    ('GRACE R', 'grace.r.cse.2024@snsce.ac.in', '', '', 'RESHMA RAJ'),
    ('HARIHARAN V', 'hariharan.v.it.2024@snsct.org', '', '', 'RESHMA RAJ'),
    ('HARIHARASUDHAN', 'harihr.k.ad.2024@snsce.ac.in', '', '', 'RESHMA RAJ'),
    ('HARISHWA', 'harishwa.ap.aiml.2024@snsct.org', '', '', 'RESHMA RAJ'),
    ('INIYAN S', 'iniyan.s.aiml.2024@snsct.org', '', '', 'RESHMA RAJ'),
    ('JABBASTIN AKASH', 'jabbastin.k.csd.2024@snsce.ac.in', '', '', 'RESHMA RAJ'),
    ('KATHIRVEL G', 'kathirvel.g.aiml.2024@snsct.org', '', '', 'RESHMA RAJ'),
    ('KAVIYA', 'kaviya.v.ad.2024@snsce.ac.in', '', '', 'RESHMA RAJ'),
    ('KAVYA S', 'kavya.s.aiml.2024@snsct.org', '', '', 'RESHMA RAJ'),
    ('LOGANA LATCHMI E', 'logana.e.cse.2024@snsce.ac.in', '', '', 'RESHMA RAJ'),
    ('MADHIYARASU R', 'madhi.r.ad.2024@snsce.ac.in', '', '', 'RESHMA RAJ'),
    ('MADHUMITHA C', 'madhum.c.ad.2024@snsce.ac.in', '', '', 'RESHMA RAJ'),
    ('MADHUSHRI S', 'madhus.s.ad.2024@snsce.ac.in', '', '', 'RESHMA RAJ'),
    ('MATHIALAGAN P', 'mathi.p.it.2024@snsce.ac.in', '', '', 'RESHMA RAJ'),
    ('MOHAMED RISWAN J', 'mohamed.j.cse.2024@snsce.ac.in', '', '', 'RESHMA RAJ'),
    ('OVIYA SRI J', 'oviyasri.j.it.2024@snsct.org', '', '', 'RESHMA RAJ'),
    ('PERUMAL A', 'perumal.a.it.2024@snsct.org', '', '', 'RESHMA RAJ'),
    ('POOJA K', 'pooja.k.iot.2024@snsce.ac.in', '', '', 'RESHMA RAJ'),
    ('PRAJITH VL', 'prajith.vl.cse.2024@snsct.org', '', '', 'RESHMA RAJ'),
    ('PRARTHANA B', 'prarthana.b.cse.2024@snsce.ac.in', '', '', 'RESHMA RAJ'),
    ('PRAVEEN S K', 'praveen.sk.cse.2024@snsct.org', '', '', 'RESHMA RAJ'),
    ('PREENA M', 'preena.m.it.2024@snsct.org', '', '', 'RESHMA RAJ'),
    ('RANJANA G', 'ranjan.g.ad.2024@snsce.ac.in', '', '', 'RESHMA RAJ'),
    ('ROSHIENI S', 'roshieni.s.csd.2024@snsce.ac.in', '', '', 'RESHMA RAJ'),
    ('SAKTHI J', 'sakthi.j.it.2024@snsct.org', '', '', 'RESHMA RAJ'),
    ('SANJANA K', 'sanjana.k.it.2024@snsct.org', '', '', 'RESHMA RAJ'),
    ('SHAKTHI SHARAAN C', 'shakthi.c.cst.2024@snsce.ac.in', '', '', 'RESHMA RAJ'),
    ('THARSHINI D J', 'tharshini.dj.aiml.2024@snsct.org', '', '', 'RESHMA RAJ'),
    ('YASWANTHIKA D S', 'yaswanthika.ds.cse.2024@snsct.org', '', '', 'RESHMA RAJ'),
    ('YATHEESHWAR M', 'yatheeshwar.m.cse.2024@snsct.org', '', '', 'RESHMA RAJ'),
    ('YOGESH M', 'yogesh.m.ad.2024@snsce.ac.in', '', '', 'RESHMA RAJ'),
    ('AENOK ANTONY C', 'aenok.ca.cse.2024@snsce.ac.in', '', '', 'TULSI KRISHNA'),
    ('AKASH G', 'akash.g.it.2024@snsct.org', '', '', 'TULSI KRISHNA'),
    ('AKSHAYA P', 'akshaya.p.it.2024@snsct.org', '', '', 'TULSI KRISHNA'),
    ('ALANA SEBASTIAN', 'alana.s.iot.2024@snsce.ac.in', '', '', 'TULSI KRISHNA'),
    ('ANU SHRI G', 'anushri.sg.aiml.2024@snsct.org', '', '', 'TULSI KRISHNA'),
    ('ARUNESH KUMAR C', 'arunesh.c.cst.2024@snsce.ac.in', '', '', 'TULSI KRISHNA'),
    ('BALAVIGNESH V T', 'bala.vt.cst.2024@snsce.ac.in', '', '', 'TULSI KRISHNA'),
    ('BHAARATHINESAN', 'bhaarathinesan.n.aiml.2024@snsct.org', '', '', 'TULSI KRISHNA'),
    ('DAYANITHI M', 'dayanithi.m.cse.2024@snsce.ac.in', '', '', 'TULSI KRISHNA'),
    ('FOUZUL HIDHAYA S SHAIK DAWOOD', 'fouzulhidhays.s.it.2024@snsct.org', '', '', 'TULSI KRISHNA'),
    ('GOWTHAM K', 'gowthm.k.ad.2024@snsce.ac.in', '', '', 'TULSI KRISHNA'),
    ('HARINI P J', 'harini.pj.it.2024@snsct.org', '', '', 'TULSI KRISHNA'),
    ('JEVESH M M', 'jevesh.mm.ad.2024@snsce.ac.in', '', '', 'TULSI KRISHNA'),
    ('KARTHIKA P', 'karthika.p.cse.2024@snsct.org', '', '', 'TULSI KRISHNA'),
    ('KAVINILA S', 'kavini.s.ad.2024@snsce.ac.in', '', '', 'TULSI KRISHNA'),
    ('KEERTHANA S', 'keerthana.s.cst.2024@snsce.ac.in', '', '', 'TULSI KRISHNA'),
    ('KIRUTHIKA', 'kiruthika.d.cse.2024@snsce.ac.in', '', '', 'TULSI KRISHNA'),
    ('KISHORE S', 'kishore.s.aiml.2024@snsct.org', '', '', 'TULSI KRISHNA'),
    ('KUMARI MASHA IVANOVNA V', 'kumari.v.ad.2024@snsce.ac.in', '', '', 'TULSI KRISHNA'),
    ('LENIN KISHOR', 'lenin.r.cst.2024@snsce.ac.in', '', '', 'TULSI KRISHNA'),
    ('LOCHANA R', 'lochan.r.ad.2024@snsce.ac.in', '', '', 'TULSI KRISHNA'),
    ('MATHIYAZHAGAN T', 'mathi.t.cse.2024@snsce.ac.in', '', '', 'TULSI KRISHNA'),
    ('MITHUN R', 'mithun.r.cse.2024@snsct.org', '', '', 'TULSI KRISHNA'),
    ('MOHAMED JAVID S', 'mohamedjavid.s.it.2024@snsct.org', '', '', 'TULSI KRISHNA'),
    ('MOHANKUMAR S', 'mohank.s.ad.2024@snsce.ac.in', '', '', 'TULSI KRISHNA'),
    ('NAREN R S', 'naren.rs.cse.2024@snsct.org', '', '', 'TULSI KRISHNA'),
    ('NAVALAKSHMI', 'navalakshmi.b.cse.2024@snsct.org', '', '', 'TULSI KRISHNA'),
    ('NAVEEN P', 'naveen.p.aiml.2024@snsct.org', '', '', 'TULSI KRISHNA'),
    ('NEHA PRIYADHARSHINI', 'neha.m.aiml.2024@snsct.org', '', '', 'TULSI KRISHNA'),
    ('NIDHINNATRAJ R', 'nidhinnatraj.r.csd.2024@snsce.ac.in', '', '', 'TULSI KRISHNA'),
    ('NITHILAA S', 'nithilaa.s.cse.2024@snsct.org', '', '', 'TULSI KRISHNA'),
    ('NIVETHITHA RAMESH', 'niveth.r.ad.2024@snsce.ac.in', '', '', 'TULSI KRISHNA'),
    ('PAULINA MARSHAL A', 'paulina.a.cse.2024@snsce.ac.in', '', '', 'TULSI KRISHNA'),
    ('PERARASU S', 'parasu.s.it.2024@snsce.ac.in', '', '', 'TULSI KRISHNA'),
    ('PHRISHA G VISWANATH', 'phrisha.gv.aiml.2024@snsct.org', '', '', 'TULSI KRISHNA'),
    ('PRATHOSH P', 'prathosh.p.aiml.2024@snsct.org', '', '', 'TULSI KRISHNA'),
    ('PRIYANKA K', 'priyan.k.ad.2024@snsce.ac.in', '', '', 'TULSI KRISHNA'),
    ('RAMKUMAR A', 'ramkr.a.ad.2024@snsce.ac.in', '', '', 'TULSI KRISHNA'),
    ('SACHIN SV', 'sachin.sv.cse.2024@snsct.org', '', '', 'TULSI KRISHNA'),
    ('SAMUKTHA S', 'samuktha.s.aiml.2024@snsct.org', '', '', 'TULSI KRISHNA'),
    ('SANTHOSH KRISHNAN M', 'santhosh.m.cse.2024@snsct.org', '', '', 'TULSI KRISHNA'),
    ('SATHY FRANCIS M', 'sathy.m.cst.2024@snsce.ac.in', '', '', 'TULSI KRISHNA'),
    ('SOWPARNIKA L S', 'sowparnika.ls.cse.2024@snsct.org', '', '', 'TULSI KRISHNA'),
    ('SRI VISHNU S', 'srivishnu.s.cse.2024@snsct.org', '', '', 'TULSI KRISHNA'),
    ('SUDHARSSHANA', 'sudharsshana.r.cse.2024@snsce.ac.in', '', '', 'TULSI KRISHNA'),
    ('TARUNYASREE H', 'tarunya.h.iot.2024@snsce.ac.in', '', '', 'TULSI KRISHNA'),
    ('VARSHANA S', 'varsha.s.ad.2024@snsce.ac.in', '', '', 'TULSI KRISHNA'),
    ('VETRI KALANJIYAM', 'vetri.b.csd.2024@snsce.ac.in', '', '', 'TULSI KRISHNA'),
    ('VISHNUDHARSHAN S', 'vishnudharshan.s.csd.2024@snsce.ac.in', '', '', 'TULSI KRISHNA'),
]


class Command(BaseCommand):
    help = 'Create all 147 students with mentor assignments from hardcoded data'

    def handle(self, *args, **options):
        self.stdout.write('========================================')
        self.stdout.write('📚 Creating all students from hardcoded data')
        self.stdout.write('========================================\n')
        
        # Create mentors first
        mentor_users = {}
        mentors_to_create = ['GOPI KRISHNAN', 'RESHMA RAJ', 'TULSI KRISHNA']
        
        for mentor_name in mentors_to_create:
            mentor_username = mentor_name.lower().replace(' ', '_')
            mentor_user, created = User.objects.get_or_create(
                username=mentor_username,
                defaults={
                    'email': f'{mentor_username}@cohortsummit.com',
                    'first_name': mentor_name.split()[0],
                    'last_name': ' '.join(mentor_name.split()[1:]) if len(mentor_name.split()) > 1 else '',
                }
            )
            if created:
                mentor_user.set_password('mentor123')
                mentor_user.save()
                self.stdout.write(f'✅ Created mentor: {mentor_name}')
            
            # Ensure mentor profile exists
            mentor_profile, _ = UserProfile.objects.get_or_create(user=mentor_user)
            mentor_profile.role = 'MENTOR'
            mentor_profile.campus = 'TECH'
            mentor_profile.floor = 2
            mentor_profile.save()
            
            mentor_users[mentor_name] = mentor_user
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('Creating students...\n')
        
        # Create students
        created_count = 0
        updated_count = 0
        error_count = 0
        
        for username, email, first_name, second_name, mentor_name in STUDENTS_DATA:
            try:
                # Parse name
                full_name = f"{first_name} {second_name}".strip() if first_name or second_name else username
                name_parts = full_name.split(' ', 1) if full_name else username.split(' ', 1)
                first = name_parts[0]
                last = name_parts[1] if len(name_parts) > 1 else ''
                
                # Create login username
                login_username = username.lower().replace(' ', '_')
                
                # Check if user exists
                existing_user = User.objects.filter(email=email).first()
                if existing_user:
                    user = existing_user
                    updated_count += 1
                else:
                    # Create new user
                    user = User.objects.create_user(
                        username=login_username,
                        email=email,
                        password='student123',
                        first_name=first,
                        last_name=last,
                    )
                    created_count += 1
                
                # Create or update profile
                profile, _ = UserProfile.objects.get_or_create(user=user)
                profile.role = 'STUDENT'
                profile.campus = 'TECH'
                profile.floor = 2
                
                # Assign mentor
                if mentor_name in mentor_users:
                    profile.assigned_mentor = mentor_users[mentor_name]
                
                profile.save()
                
            except Exception as e:
                error_count += 1
                self.stdout.write(self.style.ERROR(f'❌ Error creating {username}: {e}'))
        
        # Summary
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('✅ Student creation complete!'))
        self.stdout.write(f'   Created: {created_count} students')
        self.stdout.write(f'   Updated: {updated_count} students')
        if error_count > 0:
            self.stdout.write(self.style.WARNING(f'   Errors: {error_count}'))
        self.stdout.write(f'\n📊 Total students: {User.objects.filter(profile__role="STUDENT").count()}')
        self.stdout.write(f'📊 Total mentors: {User.objects.filter(profile__role="MENTOR").count()}')
        self.stdout.write('\nMentor distribution:')
        for mentor_name, mentor_user in mentor_users.items():
            count = UserProfile.objects.filter(assigned_mentor=mentor_user).count()
            self.stdout.write(f'   {mentor_name}: {count} students')
        self.stdout.write('=' * 60 + '\n')
