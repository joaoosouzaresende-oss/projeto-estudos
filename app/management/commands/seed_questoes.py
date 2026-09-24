from django.core.management.base import BaseCommand
from app.models import Conteudo, Questao


QUESTOES = [
    # ========== MATEMÁTICA — Funções do 1º Grau (conteudo_id=1) ==========
    {
        "conteudo_id": 1,
        "enunciado": "Se f(x) = 2x + 3, qual é o valor de f(5)?",
        "alt_a": "7",
        "alt_b": "10",
        "alt_c": "13",
        "alt_d": "15",
        "alt_e": "25",
        "resposta": "C",
        "comentario": "f(5) = 2(5) + 3 = 10 + 3 = 13. Basta substituir x por 5 na expressão da função.",
    },
    {
        "conteudo_id": 1,
        "enunciado": "A função f(x) = -3x + 9 é decrescente. Qual é o valor de x quando f(x) = 0?",
        "alt_a": "x = 3",
        "alt_b": "x = -3",
        "alt_c": "x = 9",
        "alt_d": "x = 0",
        "alt_e": "x = 6",
        "resposta": "A",
        "comentario": "Para encontrar o zero da função, igualamos f(x) = 0: -3x + 9 = 0 → -3x = -9 → x = 3.",
    },
    {
        "conteudo_id": 1,
        "enunciado": "Qual é o coeficiente angular da função f(x) = -5x + 2?",
        "alt_a": "2",
        "alt_b": "-2",
        "alt_c": "5",
        "alt_d": "-5",
        "alt_e": "7",
        "resposta": "D",
        "comentario": "Na função f(x) = ax + b, o coeficiente angular é o número que multiplica x. Aqui, a = -5.",
    },
    {
        "conteudo_id": 1,
        "enunciado": "Se f(x) = 3x - 2, qual é o valor de x quando f(x) = 10?",
        "alt_a": "x = 2",
        "alt_b": "x = 3",
        "alt_c": "x = 4",
        "alt_d": "x = 5",
        "alt_e": "x = 6",
        "resposta": "C",
        "comentario": "Igualando f(x) = 10: 3x - 2 = 10 → 3x = 12 → x = 4.",
    },
    {
        "conteudo_id": 1,
        "enunciado": "Uma função do 1º grau tem coeficiente angular igual a 2 e passa pelo ponto (1, 5). Qual é a expressão da função?",
        "alt_a": "f(x) = 2x + 3",
        "alt_b": "f(x) = 2x + 5",
        "alt_c": "f(x) = 2x - 3",
        "alt_d": "f(x) = 2x + 1",
        "alt_e": "f(x) = 2x - 1",
        "resposta": "A",
        "comentario": "Sabendo que f(x) = 2x + b e que f(1) = 5: 5 = 2(1) + b → b = 3. Logo, f(x) = 2x + 3.",
    },
    {
        "conteudo_id": 1,
        "enunciado": "Qual é o coeficiente linear da função f(x) = -x + 7?",
        "alt_a": "-1",
        "alt_b": "1",
        "alt_c": "7",
        "alt_d": "-7",
        "alt_e": "0",
        "resposta": "C",
        "comentario": "Na função f(x) = ax + b, o coeficiente linear é o termo independente (b). Aqui, b = 7.",
    },

    # ========== LÍNGUA PORTUGUESA — Interpretação de Texto (conteudo_id=2) ==========
    {
        "conteudo_id": 2,
        "enunciado": "Leia o trecho: 'O silêncio da noite foi quebrado pelo canto distante de um pássaro.' Qual o sentido da expressão 'quebrado' nesse contexto?",
        "alt_a": "Destruição física",
        "alt_b": "Interrupção do silêncio",
        "alt_c": "Rompimento de um objeto",
        "alt_d": "Violência contra o pássaro",
        "alt_e": "Morte do pássaro",
        "resposta": "B",
        "comentario": "O sentido de 'quebrado' aqui é figurado: o canto do pássaro interrompeu o silêncio. Não há destruição física.",
    },
    {
        "conteudo_id": 2,
        "enunciado": "Em um texto argumentativo, qual é a função principal de um dado estatístico apresentado em um parágrafo?",
        "alt_a": "Enfeitar o texto",
        "alt_b": "Amamentar o leitor",
        "alt_c": "Comprovar uma ideia com dados concretos",
        "alt_d": "Substituir a opinião do autor",
        "alt_e": "Aumentar o tamanho do texto",
        "resposta": "C",
        "comentario": "Dados estatísticos servem como argumento de autoridade, comprovando o que o autor afirma com números reais.",
    },
    {
        "conteudo_id": 2,
        "enunciado": "Na frase 'Embora estivesse cansado, ele continuou trabalhando', qual é a relação de sentido entre as orações?",
        "alt_a": "Causa",
        "alt_b": "Consequência",
        "alt_c": "Oposição",
        "alt_d": "Temporal",
        "alt_e": "Concessiva",
        "resposta": "E",
        "comentario": "A conjunção 'embora' introduz uma oração concessiva: apesar de estar cansado (concessão), ele continuou trabalhando.",
    },
    {
        "conteudo_id": 2,
        "enunciado": "Qual das alternativas apresenta um erro de coesão textual?",
        "alt_a": "Ele estudou muito. Por isso, foi aprovado.",
        "alt_b": "Ele estudou muito. Embora, foi aprovado.",
        "alt_c": "Ele estudou muito e foi aprovado.",
        "alt_d": "Ele estudou muito. Logo, foi aprovado.",
        "alt_e": "Ele estudou muito. Portanto, foi aprovado.",
        "resposta": "B",
        "comentario": "'Embora' é uma conjunção concessiva e não pode ser usada como 'por isso'. O correto seria 'Por isso, foi aprovado' ou 'Embora estivesse cansado, foi aprovado'.",
    },
    {
        "conteudo_id": 2,
        "enunciado": "No período 'O livro que li ontem era fascinante', a palavra 'que' funciona como:",
        "alt_a": "Pronome relativo",
        "alt_b": "Conjunção integrante",
        "alt_c": "Conjunção explicativa",
        "alt_d": "Advérbio",
        "alt_e": "Preposição",
        "resposta": "A",
        "comentario": "'Que' é um pronome relativo que se refere a 'livro' e liga a oração subordinada à principal.",
    },

    # ========== HISTÓRIA — Revolução Industrial (conteudo_id=3) ==========
    {
        "conteudo_id": 3,
        "enunciado": "Em qual país a Revolução Industrial teve início, no final do século XVIII?",
        "alt_a": "França",
        "alt_b": "Alemanha",
        "alt_c": "Estados Unidos",
        "alt_d": "Inglaterra",
        "alt_e": "Itália",
        "resposta": "D",
        "comentario": "A Revolução Industrial começou na Inglaterra por volta de 1760, impulsionada pela mecanização da indústria têxtil e pela availability de carvão mineral.",
    },
    {
        "conteudo_id": 3,
        "enunciado": "Qual invento foi fundamental para a mecanização da indústria têxtil durante a Revolução Industrial?",
        "alt_a": "Máquina a vapor",
        "alt_b": "Teares mecânicos",
        "alt_c": "Motor de combustão",
        "alt_d": "Telegrafo",
        "alt_e": "Ferrovia",
        "resposta": "B",
        "comentario": "Os teares mecânicos (como o de James Hargreaves) revolucionaram a tecelagem, permitindo produção em larga escala. A máquina a vapor (A) era usada como fonte de energia, mas o tear foi o inventor-chave da têxtil.",
    },
    {
        "conteudo_id": 3,
        "enunciado": "A Revolução Industrial provocou:",
        "alt_a": "Diminuição do trabalho infantil",
        "alt_b": "Migração do campo para a cidade (urbanização)",
        "alt_c": "Aumento da produção artesanal",
        "alt_d": "Fim da exploração dos trabalhadores",
        "alt_e": "Redução da poluição nas cidades",
        "resposta": "B",
        "comentario": "A Revolução Industrial acelerou a urbanização: trabalhadores deixaram o campo para trabalhar nas fábricas, gerando crescimento desordenado das cidades.",
    },
    {
        "conteudo_id": 3,
        "enunciado": "Quem aperfeiçoou a máquina a vapor, tornando-a viável para uso industrial no final do século XVIII?",
        "alt_a": "Thomas Edison",
        "alt_b": "Henry Ford",
        "alt_c": "James Watt",
        "alt_d": "Alexander Graham Bell",
        "alt_e": "Benjamin Franklin",
        "resposta": "C",
        "comentario": "James Watt aperfeiçoou a máquina a vapor de Newcomen em 1769, tornando-a eficiente o suficiente para movimentar máquinas industriais.",
    },
    {
        "conteudo_id": 3,
        "enunciado": "A exploração do trabalho infantil nas fábricas da Revolução Industrial é um exemplo de:",
        "alt_a": "Progresso social",
        "alt_b": "Desigualdade social e trabalho análogo à escravidão",
        "alt_c": "Democratização do trabalho",
        "alt_d": "Melhoria das condições de vida",
        "alt_e": "Evolução tecnológica positiva",
        "resposta": "B",
        "comentario": "Crianças trabalhavam 12-16 horas por dia em condições precárias, sem direitos. Isso evidencia a desigualdade social gerada pelo capitalismo industrial.",
    },
]


class Command(BaseCommand):
    help = "Popula o banco com questões de nível ENEM"

    def handle(self, *args, **options):
        criadas = 0
        for dados in QUESTOES:
            conteudo = Conteudo.objects.get(id=dados["conteudo_id"])
            questao, created = Questao.objects.get_or_create(
                conteudo=conteudo,
                enunciado=dados["enunciado"],
                defaults={
                    "alt_a": dados["alt_a"],
                    "alt_b": dados["alt_b"],
                    "alt_c": dados["alt_c"],
                    "alt_d": dados["alt_d"],
                    "alt_e": dados["alt_e"],
                    "resposta": dados["resposta"],
                    "comentario": dados["comentario"],
                },
            )
            if created:
                criadas += 1
                self.stdout.write(f"  + Questão #{questao.pk} ({conteudo.materia.nome})")
            else:
                self.stdout.write(f"  = Questão já existe ({conteudo.materia.nome})")

        self.stdout.write(self.style.SUCCESS(f"\n{criadas} questão(ões) criada(s) com sucesso!"))
