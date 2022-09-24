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
        text="Antes que nada dime que te parece la vacante a la que te postulaste:\n\nEl auxiliar de almacén colabora en el almacenaje de productos perecederos, el armado de pedidos, orden y limpieza del almacén, entre otras cosas.\nSe trabaja 6 días por semana, con 1 de descanso, en tres turnos rolados.\nEl puesto cuenta con un atractivo sueldo base y prestaciones superiores a las de la ley.",
        options = ["Me interesa","+ info","No me interesa"],
        ).get_dict()

    preguntaMoreInfo = Question(
        index="more_info",
        text="Claro! Te puedo contar más 😊\n\nSomos una compañía global dedicada a ofrecer los alimentos favoritos de las comunidades. Con presencia en 18 países, ofrecemos productos de calidad en diversas categorías y precios.",
        options = ["Me interesa","No me interesa"],
        exactMatch=False,       
    ).get_dict()

    preguntaNoInterest = Question(
        index="no_interest",
        text = "Entiendo. No hay problema! Si en algún momento cambias de opinión me puedes esrcibir nuevamente. Adiós!",
        immediateNext = True,
    ).get_dict()

    preguntaInterestBye = Question(
    	index ='interest_bye',
    	text = 'Genial! 💪 Te tendré en cuenta para el puesto. Que tengas un gran día',
    	immediateNext = True,
    ).get_dict()


    # Armado de secuencia
    preguntaIntro["question"]["connections"].append({'goto':preguntaQuienEsEmi["question"]["index"], 'isString': "Quién es Emi?"})
    preguntaIntro["question"]["connections"].append({'goto':preguntaInterest["question"]["index"], 'isString': "Si"})

    preguntaInterest["question"]["connections"].append({'goto':preguntaMoreInfo["question"]["index"], 'isString': "+ info"})

    
    preguntaQuienEsEmi["question"]["connections"].append({'goto':preguntaSosUnRobot["question"]["index"], 'isString': "Eres un robot?"})
    preguntaQuienEsEmi["question"]["connections"].append({'goto':preguntaInterest["question"]["index"], 'isDefault': True})

    preguntaSosUnRobot["question"]["connections"].append({'goto':preguntaInterest["question"]["index"], 'isDefault': True})

    preguntaIntro["question"]["connections"].append({'goto':preguntaNoInterest["question"]["index"], 'isString': "No me interesa"})
    preguntaInterest["question"]["connections"].append({'goto':preguntaNoInterest["question"]["index"], 'isString': "No me interesa"})
    preguntaInterest["question"]["connections"].append({'goto':preguntaInterestBye["question"]["index"], 'isDefault': True})
    preguntaQuienEsEmi["question"]["connections"].append({'goto':preguntaNoInterest["question"]["index"], 'isString': "No me interesa"})
    preguntaSosUnRobot["question"]["connections"].append({'goto':preguntaNoInterest["question"]["index"], 'isString': "No me interesa"})
    preguntaMoreInfo["question"]["connections"].append({'goto':preguntaInterestBye["question"]["index"], 'isDefault': True})
    preguntaMoreInfo["question"]["connections"].append({'goto':preguntaNoInterest["question"]["index"], 'isString': "No me interesa"})


    # Armado de set de schedule
    flow["current"] = preguntaIntro["question"]["index"]
    flow[preguntaIntro["question"]["index"]] = preguntaIntro
    flow[preguntaQuienEsEmi["question"]["index"]] = preguntaQuienEsEmi
    flow[preguntaSosUnRobot["question"]["index"]] = preguntaSosUnRobot
    flow[preguntaInterest["question"]["index"]] = preguntaInterest
    flow[preguntaMoreInfo["question"]["index"]] = preguntaMoreInfo
    flow[preguntaNoInterest["question"]["index"]] = preguntaNoInterest
    flow[preguntaInterestBye["question"]["index"]] = preguntaInterestBye

    return flow


def get_test_flow():
	return getFlow()


if __name__ == '__main__':
    import json
    print(json.dumps(get_test_flow()))

