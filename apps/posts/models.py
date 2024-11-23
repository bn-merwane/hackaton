from django.db import models
from apps.accounts.models import Account


WILAYA_CHOICES = [
    ('01', 'Adrar'),
    ('02', 'Chlef'),
    ('03', 'Laghouat'),
    ('04', 'Oum El Bouaghi'),
    ('05', 'Batna'),
    ('06', 'Béjaïa'),
    ('07', 'Biskra'),
    ('08', 'Béchar'),
    ('09', 'Blida'),
    ('10', 'Bouira'),
    ('11', 'Tamanrasset'),
    ('12', 'Tébessa'),
    ('13', 'Tlemcen'),
    ('14', 'Tiaret'),
    ('15', 'Tizi Ouzou'),
    ('16', 'Alger'),
    ('17', 'Djelfa'),
    ('18', 'Jijel'),
    ('19', 'Sétif'),
    ('20', 'Saïda'),
    ('21', 'Skikda'),
    ('22', 'Sidi Bel Abbès'),
    ('23', 'Annaba'),
    ('24', 'Guelma'),
    ('25', 'Constantine'),
    ('26', 'Médéa'),
    ('27', 'Mostaganem'),
    ('28', 'M’Sila'),
    ('29', 'Mascara'),
    ('30', 'Ouargla'),
    ('31', 'Oran'),
    ('32', 'El Bayadh'),
    ('33', 'Illizi'),
    ('34', 'Bordj Bou Arréridj'),
    ('35', 'Boumerdès'),
    ('36', 'El Tarf'),
    ('37', 'Tindouf'),
    ('38', 'Tissemsilt'),
    ('39', 'El Oued'),
    ('40', 'Khenchela'),
    ('41', 'Souk Ahras'),
    ('42', 'Tipaza'),
    ('43', 'Mila'),
    ('44', 'Aïn Defla'),
    ('45', 'Naâma'),
    ('46', 'Aïn Témouchent'),
    ('47', 'Ghardaïa'),
    ('48', 'Relizane'),
    ('49', 'Timimoun'),
    ('50', 'Bordj Badji Mokhtar'),
    ('51', 'Ouled Djellal'),
    ('52', 'Béni Abbès'),
    ('53', 'In Salah'),
    ('54', 'In Guezzam'),
    ('55', 'Touggourt'),
    ('56', 'Djanet'),
    ('57', 'El M’Ghair'),
    ('58', 'El Meniaa'),
]



class Post(models.Model):
    name = models.CharField(
        max_length=250,
        null=False,
        blank=False,
        help_text="Name of the post office or establishment."
    )
    code_postale = models.PositiveBigIntegerField(
        null=False,
        blank=False,
        help_text="Postal code of the post office."
    )

    wilaya = models.CharField(
        max_length=2,
        choices=WILAYA_CHOICES,
        null=False,
        blank=False,
        help_text="Wilaya where the post office is located."
    )
    address = models.TextField(
        null=False,
        blank=False,
        help_text="Full address of the post office."
    )
    heure_debut_hiver = models.CharField(
        max_length=150,
        null=False,
        blank=False,
        help_text="Opening time during winter."
    )
    heure_fin_hiver = models.CharField(
        max_length=150,
        null=False,
        blank=False,
        help_text="Closing time during winter."
    )
    heure_debut_ete = models.CharField(
        max_length=150,
        null=False,
        blank=False,
        help_text="Opening time during summer."
    )
    heure_fin_ete = models.CharField(
        max_length=150,
        null=False,
        blank=False,
        help_text="Closing time during summer."
    )

    employees = models.ManyToManyField(Account,null=True)

    has_distrubuteur = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['wilaya', 'code_postale']

    def __str__(self):
        return f"{self.name} ({self.get_wilaya_display()})"
