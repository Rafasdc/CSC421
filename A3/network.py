#Problem 3

from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

music_model = BayesianModel([('Difficulty','Rating'),
						('Musicianship', 'Rating'),
						('Musicianship','Exam'),
						('Rating','Letter')	])

rating_cpd = TabularCPD(
			variable='Rating',
			variable_card = 3,
			values = [[0.3,0.05,0.9,0.5],
					  [0.4,0.25,0.08,0.3],
					  [0.3,0.7,0.02,0.2]],
			evidence=['Difficulty',"Musicianship"],
			evidence_card=[2,2])

difficulty_cpd = TabularCPD(
			variable='Difficulty',
			variable_card=2,
			values=[[0.6,0.4]])

musicianship_cpd = TabularCPD(
			variable = 'Musicianship',
			variable_card=2,
			values=[[0.7,0.3]])

letter_cpd = TabularCPD(
			variable = 'Letter',
			variable_card=2,
			values=[[0.1,0.4,0.99],
					[0.9,0.6,0.01]],
			evidence=['Rating'],
			evidence_card=[3])

exam_cpd = TabularCPD(
			variable='Exam',
			variable_card=2,
			values=[[0.95,0.2],
					[0.05,0.8]],
			evidence=['Musicianship'],
			evidence_card=[2])

print(rating_cpd)
print(difficulty_cpd)
print(musicianship_cpd)
print(letter_cpd)
print(exam_cpd)

print(music_model.edges())


music_model.add_cpds(rating_cpd,difficulty_cpd,musicianship_cpd,letter_cpd,exam_cpd)

print(music_model.get_cpds())

print(music_model.check_model())

music_infer = VariableElimination(music_model)

m_1 = music_infer.query(variables=['Musicianship'])
print(m_1['Musicianship'])

d_l = music_infer.query(variables=['Difficulty'])
print(d_l['Difficulty'])

r_2s_g_m_s_d_l = music_infer.query(variables=['Rating'],evidence={'Musicianship':1,'Difficulty':0})
print(r_2s_g_m_s_d_l['Rating'])

p_e = music_infer.query(variables=['Exam'],evidence={'Musicianship':1})
print(p_e['Exam'])

p_l_w_g_r_2_s = music_infer.query(variables=['Letter'],evidence={'Rating':1})
print(p_l_w_g_r_2_s['Letter'])

#Proabiblity Letter is Strong, given no other information
p_l_s = music_infer.query(variables=['Letter'])
print(p_l_s['Letter'])

#Probability Letter is Strong, given not strong musician.
p_l_s_m_w = music_infer.query(variables=['Letter'],evidence={'Musicianship':0})
print(p_l_s_m_w['Letter'])

#m_1 = music_infer.map_query(variables=['Musicianship'],evidence={'Musicianship':1})




'''
			values=[[0.3,0.4,0.3],
					[0.05,0.25,0.7],
					[0.9,0.08,0.02],
					[0.5,0.3,0.2]],

'''
