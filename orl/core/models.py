from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

CHOICES_PROBLEMAS = (
    ('1', 'Ivan: o cientista maluco'),
    ('2', 'Parece lógica'),
    ('3', 'Campeonato de UÓ'),
    ('4', 'Facebook e o granjeiro'),
    ('5', 'Italiano'),
    ('6', 'Capitão Saraiva'),
    ('7', 'Figuras'),
    ('8', 'Cálculos Diversos'),
    ('9', 'Cidade Alfa'),
    ('10', 'LauBot'),
)

CHOICES_CONDICAO = (
    ('RE', 'RECUSADO'),
    ('AC', 'ACEITO')
)
'''
print("CHOICES_EQUIPES = (")
for x in range(1, 81):
    print("('"+str(x)+"', '" + str(x) + ' - Equipe ' + str(x) +"'),")
print(")")
'''
CHOICES_EQUIPES = (
    ('1', '1 - Equipe 1'),
    ('2', '2 - Equipe 2'),
    ('3', '3 - Equipe 3'),
    ('4', '4 - Equipe 4'),
    ('5', '5 - Equipe 5'),
    ('6', '6 - Equipe 6'),
    ('7', '7 - Equipe 7'),
    ('8', '8 - Equipe 8'),
    ('9', '9 - Equipe 9'),
    ('10', '10 - Equipe 10'),
    ('11', '11 - Equipe 11'),
    ('12', '12 - Equipe 12'),
    ('13', '13 - Equipe 13'),
    ('14', '14 - Equipe 14'),
    ('15', '15 - Equipe 15'),
    ('16', '16 - Equipe 16'),
    ('17', '17 - Equipe 17'),
    ('18', '18 - Equipe 18'),
    ('19', '19 - Equipe 19'),
    ('20', '20 - Equipe 20'),
    ('21', '21 - Equipe 21'),
    ('22', '22 - Equipe 22'),
    ('23', '23 - Equipe 23'),
    ('24', '24 - Equipe 24'),
    ('25', '25 - Equipe 25'),
    ('26', '26 - Equipe 26'),
    ('27', '27 - Equipe 27'),
    ('28', '28 - Equipe 28'),
    ('29', '29 - Equipe 29'),
    ('30', '30 - Equipe 30'),
    ('31', '31 - Equipe 31'),
    ('32', '32 - Equipe 32'),
    ('33', '33 - Equipe 33'),
    ('34', '34 - Equipe 34'),
    ('35', '35 - Equipe 35'),
    ('36', '36 - Equipe 36'),
    ('37', '37 - Equipe 37'),
    ('38', '38 - Equipe 38'),
    ('39', '39 - Equipe 39'),
    ('40', '40 - Equipe 40'),
    ('41', '41 - Equipe 41'),
    ('42', '42 - Equipe 42'),
    ('43', '43 - Equipe 43'),
    ('44', '44 - Equipe 44'),
    ('45', '45 - Equipe 45'),
    ('46', '46 - Equipe 46'),
    ('47', '47 - Equipe 47'),
    ('48', '48 - Equipe 48'),
    ('49', '49 - Equipe 49'),
    ('50', '50 - Equipe 50'),
    ('51', '51 - Equipe 51'),
    ('52', '52 - Equipe 52'),
    ('53', '53 - Equipe 53'),
    ('54', '54 - Equipe 54'),
    ('55', '55 - Equipe 55'),
    ('56', '56 - Equipe 56'),
    ('57', '57 - Equipe 57'),
    ('58', '58 - Equipe 58'),
    ('59', '59 - Equipe 59'),
    ('60', '60 - Equipe 60'),
    ('61', '61 - Equipe 61'),
    ('62', '62 - Equipe 62'),
    ('63', '63 - Equipe 63'),
    ('64', '64 - Equipe 64'),
    ('65', '65 - Equipe 65'),
    ('66', '66 - Equipe 66'),
    ('67', '67 - Equipe 67'),
    ('68', '68 - Equipe 68'),
    ('69', '69 - Equipe 69'),
    ('70', '70 - Equipe 70'),
    ('71', '71 - Equipe 71'),
    ('72', '72 - Equipe 72'),
    ('73', '73 - Equipe 73'),
    ('74', '74 - Equipe 74'),
    ('75', '75 - Equipe 75'),
    ('76', '76 - Equipe 76'),
    ('77', '77 - Equipe 77'),
    ('78', '78 - Equipe 78'),
    ('79', '79 - Equipe 79'),
    ('80', '80 - Equipe 80'),
)


class SubmissaoModel(models.Model):
    problema = models.CharField(
        verbose_name='Problema',
        max_length=2,
        choices=CHOICES_PROBLEMAS,
        default='1'
    )
    equipe = models.CharField(
        verbose_name='Equipe',
        max_length=3,
        choices=CHOICES_EQUIPES,
    )
    tempo = models.IntegerField(
        verbose_name='Tempo de entrega',
        blank=False,
        validators=[MinValueValidator(1), MaxValueValidator(200), ],
    )
    status = models.CharField(
        verbose_name='Status',
        max_length=2,
        choices=CHOICES_CONDICAO,
    )
    modificado_em = models.DateTimeField(
        verbose_name='modificado em',
        auto_now_add=False,
        auto_now=True
    )
