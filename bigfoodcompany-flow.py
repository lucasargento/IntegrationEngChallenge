# -*- coding: utf-8 -*-

class Question():
	def __init__(self, index='', text='', options=[], errorMessageNotMatch=None, exactMatch=None, immediateNext=False):
		self.index = index
		self.text = text
		self.options = options
		self.errorMessageNotMatch = errorMessageNotMatch
		self.exactMatch = exactMatch
		self.immediateNext = immediateNext

	def get_dict(self):
		return {
			'question': {
				'index': self.index,
				'text': self.text,
				'options': self.options,
				'errorMessageNotMatch': self.errorMessageNotMatch,
				'exactMatch': self.exactMatch,
				'connections': []
			}
		}


def getFlow():
    flow = {}

    preguntaIntro = Question(
        index="intro",
        text="Para poder completar tu postulación para el puesto de Auxiliar de Almacén en la empresa BigFoodCompany, necesito hacerte unas preguntas para entender tu perfil. No te preocupes, son menos de 5 minutos ⏰\n\n ¿Comenzamos?",
        options=["Si", "Quién es Emi?", "No me interesa"],
        errorMessageNotMatch="Creo que no te he entendido 🤔... Prueba con las opciones que te doy",
        exactMatch=False,
    ).get_dict()

    preguntaQuienEsEmi = Question(
        index="quienEsEmi",
        text="Soy un asistente virtual e intentaré ayudarte cada vez que te postules a un puesto de trabajo. La conversación conmigo no reemplaza una entrevista en persona,"
             " sino que mi objetivo es que tu perfil sea analizado y tomado en cuenta para este puesto y que puedas tener una oportunidad justa de conseguirlo!",
        options=["Ok, empecemos!", "Eres un robot?","No me interesa"],
        ).get_dict()

    preguntaSosUnRobot = Question(
        index="sosUnRobot",
        text="Sí! 🤖 Intentaré entender lo que me dices con todo mi esfuerzo, pero no siempre lo logro 😕 Con un poco de paciencia vamos a poder completar tu aplicación rápidamente 😄",
        errorMessageNotMatch="Creo que no te he entendido 🤔... Intenta con las opciones que te doy",
        exactMatch=True,
        options=["Ok, empecemos!", "No me interesa"],       
      ).get_dict()

    preguntaInterest = Question(
        index="interest",
        text="Antes que nada dime que te parece la vacante a la que te postulaste:\n\nEl auxiliar de almacén colabora en el almacenaje de productos perecederos, el armado de pedidos, orden y limpieza del almacén, entre otras cosas.\nSe trabaja 6 días por semana, con 1 de descanso, en tres turnos rolados.\nEl puesto cuenta con un sueldo mensual que ronda entre $5,000 y $7,000 pesos y prestaciones superiores a las de la ley",
        options = ["Me interesa","+ info","No me interesa"],
        ).get_dict()

    # Nueva pregunta
    preguntaDeAcuerdo = Question(
        index = "de_acuerdo",
        text = "Todas tus respuestas serán recolectadas y entregadas al equipo de Recursos Humanos de BigFoodCompany. Estás de acuerdo?",
        options = ["Si", "No"]
    ).get_dict()

    preguntaMoreInfo = Question(
        index="more_info",
        text="Claro! Te puedo contar más 😊\n\nSomos una compañía global dedicada a ofrecer los alimentos favoritos de las comunidades. Con presencia en 18 países, ofrecemos productos de calidad en diversas categorías y precios.",
        options = ["Me interesa","No me interesa"],
        exactMatch=False,       
    ).get_dict()

    preguntaNoInterest = Question(
        index="no_interest",
        text = "Entiendo. No hay problema! Si en algún momento cambias de opinión me puedes escribir nuevamente. Adiós!",
        immediateNext = True,
        options = ["Quiero volver a empezar","Adios!"],
    ).get_dict()

    preguntaInterestBye = Question(
    	index ='interest_bye',
    	text = 'Genial! 💪 Te tendré en cuenta para el puesto. Que tengas un gran día',
    	immediateNext = True,
    ).get_dict()


    # Armado de secuencia

    # Connections de pregunta intro. Presentacion de Emi
    preguntaIntro["question"]["connections"].append({'goto':preguntaQuienEsEmi["question"]["index"], 'isString': "Quién es Emi?"})
    preguntaIntro["question"]["connections"].append({'goto':preguntaInterest["question"]["index"], 'isString': "Si"})
    preguntaIntro["question"]["connections"].append({'goto':preguntaNoInterest["question"]["index"], 'isString': "No me interesa"})
    
    # Connections de pregunta quien es Emi. puede venir aca desde la intro si el candidato quiere saber mas sobre emi
    preguntaQuienEsEmi["question"]["connections"].append({'goto':preguntaSosUnRobot["question"]["index"], 'isString': "Eres un robot?"})
    preguntaQuienEsEmi["question"]["connections"].append({'goto':preguntaInterest["question"]["index"], 'isDefault': True})
    preguntaQuienEsEmi["question"]["connections"].append({'goto':preguntaNoInterest["question"]["index"], 'isString': "No me interesa"})

    # Connections de pregunta sos un robot.
    preguntaSosUnRobot["question"]["connections"].append({'goto':preguntaInterest["question"]["index"], 'isDefault': True})
    preguntaSosUnRobot["question"]["connections"].append({'goto':preguntaNoInterest["question"]["index"], 'isString': "No me interesa"})

    # Connections de pregunta interest. Emi le pregunta al candidato si esta interesado en la posicion. Si esta interesado le pide confirmacion, sino lo saluda. Tambien puede darle mas info
    preguntaInterest["question"]["connections"].append({'goto':preguntaMoreInfo["question"]["index"], 'isString': "+ info"}) # mas info
    preguntaInterest["question"]["connections"].append({'goto':preguntaNoInterest["question"]["index"], 'isString': "No me interesa"}) # no le interesa
    preguntaInterest["question"]["connections"].append({'goto':preguntaDeAcuerdo["question"]["index"], 'isDefault': True}) # Le pregunta si esta de acuerdo!
    
    # Connections de pregunta mas info 
    preguntaMoreInfo["question"]["connections"].append({'goto':preguntaDeAcuerdo["question"]["index"], 'isDefault': True}) # si dijo que le interesaba, despues de pedir mas info, tambien hay que preguntarle si esta de acuerdo!
    preguntaMoreInfo["question"]["connections"].append({'goto':preguntaNoInterest["question"]["index"], 'isString': "No me interesa"}) # si no le interesa bye

    # Connections de pregunta de acuerdo. Si no esta de acuerdo con que se compartan sus datos, lo saluda. Si esta de acuerdo pasa a la pregunta interest.
    preguntaDeAcuerdo["question"]["connections"].append({'goto':preguntaInterestBye["question"]["index"], 'isString': "Si"}) # si esta de acuerdo, Emi confirma la postulacion y saluda
    preguntaDeAcuerdo["question"]["connections"].append({'goto':preguntaNoInterest["question"]["index"], 'isString': "No"}) # si no esta de acuerdo, emi le dice que todo ok

    # Connections de la pregunta No interest. Le vamos a dar la posibilidad de empezar de vuelta por si se arrepintió o equivocó
    preguntaNoInterest["question"]["connections"].append({'goto':preguntaIntro["question"]["index"], 'isString': "Quiero volver a empezar"}) 

    # Armado de set de schedule, con nueva pregunta agregada
    flow["current"] = preguntaIntro["question"]["index"]
    flow[preguntaIntro["question"]["index"]] = preguntaIntro
    flow[preguntaQuienEsEmi["question"]["index"]] = preguntaQuienEsEmi
    flow[preguntaSosUnRobot["question"]["index"]] = preguntaSosUnRobot
    flow[preguntaInterest["question"]["index"]] = preguntaInterest
    flow[preguntaDeAcuerdo["question"]["index"]] = preguntaDeAcuerdo
    flow[preguntaMoreInfo["question"]["index"]] = preguntaMoreInfo
    flow[preguntaNoInterest["question"]["index"]] = preguntaNoInterest
    flow[preguntaInterestBye["question"]["index"]] = preguntaInterestBye

    return flow


def get_test_flow():
	return getFlow()


if __name__ == '__main__':
    import json
    flow = get_test_flow()
    with open("modified_output_flow.json", "w",encoding='utf8') as write_file:
        json.dump(flow, write_file, indent=4,ensure_ascii=False)
    #print(json.dumps(flow))
    print("Output flow saved to disk :)")

