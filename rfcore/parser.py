from rply import ParserGenerator
from rfcore.rf_ast import Number, Sum, Sub, Stdout


class Parser:
	def __init__(self, module, builder, printf):
		self.pg = ParserGenerator(
			# Список всех токенов, принятых парсером.
			['NUMBER', 'STDOUT', 'OPEN_PAREN', 'CLOSE_PAREN',
			 'SEMI_COLON', 'SUM', 'SUB']
		)
		self.module = module
		self.builder = builder
		self.printf = printf

	def parse(self):
		@self.pg.production('program : STDOUT OPEN_PAREN expression CLOSE_PAREN SEMI_COLON')
		def program(p):
			return Stdout(self.builder, self.module, self.printf, p[2])

		@self.pg.production('expression : expression SUM expression')
		@self.pg.production('expression : expression SUB expression')
		def expression(p):
			left = p[0]
			right = p[2]
			operator = p[1]
			if operator.gettokentype() == 'SUM':
				return Sum(self.builder, self.module, left, right)
			elif operator.gettokentype() == 'SUB':
				return Sub(self.builder, self.module, left, right)

		@self.pg.production('expression : NUMBER')
		def number(p):
			return Number(self.builder, self.module, p[0].value)

		@self.pg.error
		def error_handle(token):
			raise ValueError(token)

	def get_parser(self):
		return self.pg.build()
