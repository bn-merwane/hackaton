# Generated by Django 5.1.2 on 2024-11-20 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the post office or establishment.', max_length=250)),
                ('code_postale', models.PositiveBigIntegerField(help_text='Postal code of the post office.')),
                ('wilaya', models.CharField(choices=[('01', 'Adrar'), ('02', 'Chlef'), ('03', 'Laghouat'), ('04', 'Oum El Bouaghi'), ('05', 'Batna'), ('06', 'Béjaïa'), ('07', 'Biskra'), ('08', 'Béchar'), ('09', 'Blida'), ('10', 'Bouira'), ('11', 'Tamanrasset'), ('12', 'Tébessa'), ('13', 'Tlemcen'), ('14', 'Tiaret'), ('15', 'Tizi Ouzou'), ('16', 'Alger'), ('17', 'Djelfa'), ('18', 'Jijel'), ('19', 'Sétif'), ('20', 'Saïda'), ('21', 'Skikda'), ('22', 'Sidi Bel Abbès'), ('23', 'Annaba'), ('24', 'Guelma'), ('25', 'Constantine'), ('26', 'Médéa'), ('27', 'Mostaganem'), ('28', 'M’Sila'), ('29', 'Mascara'), ('30', 'Ouargla'), ('31', 'Oran'), ('32', 'El Bayadh'), ('33', 'Illizi'), ('34', 'Bordj Bou Arréridj'), ('35', 'Boumerdès'), ('36', 'El Tarf'), ('37', 'Tindouf'), ('38', 'Tissemsilt'), ('39', 'El Oued'), ('40', 'Khenchela'), ('41', 'Souk Ahras'), ('42', 'Tipaza'), ('43', 'Mila'), ('44', 'Aïn Defla'), ('45', 'Naâma'), ('46', 'Aïn Témouchent'), ('47', 'Ghardaïa'), ('48', 'Relizane'), ('49', 'Timimoun'), ('50', 'Bordj Badji Mokhtar'), ('51', 'Ouled Djellal'), ('52', 'Béni Abbès'), ('53', 'In Salah'), ('54', 'In Guezzam'), ('55', 'Touggourt'), ('56', 'Djanet'), ('57', 'El M’Ghair'), ('58', 'El Meniaa')], help_text='Wilaya where the post office is located.', max_length=2)),
                ('address', models.TextField(help_text='Full address of the post office.')),
                ('heure_debut_hiver', models.CharField(help_text='Opening time during winter.', max_length=150)),
                ('heure_fin_hiver', models.CharField(help_text='Closing time during winter.', max_length=150)),
                ('heure_debut_ete', models.CharField(help_text='Opening time during summer.', max_length=150)),
                ('heure_fin_ete', models.CharField(help_text='Closing time during summer.', max_length=150)),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
                'ordering': ['wilaya', 'code_postale'],
            },
        ),
    ]