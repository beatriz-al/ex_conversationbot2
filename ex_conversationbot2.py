# pip install aiogram
import asyncio
import requests
from aiogram import Bot, Dispatcher, executor, types
import random
from telegram import Chat, KeyboardButton, ReplyKeyboardMarkup

API_TOKEN = 'TOKEN'


# Inicializa bot e dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

res = []
dados = []


# Trata as informações recebidas
async def facts_to_str(res: list):
    for i in res[1::2]:
        out = str(f'{res[0]} - {res[1]}')
        print(f'\r\Informações:: {out}')
        res.remove(res[0])
        res.remove(res[0])
        dados.append(out)
    return dados

keyboard_markup = types.ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True, row_width=1)

btns_text = ('Idade', 'Cor favorita', 'Número de irmãos',
             'Outra coisa...', 'Feito')
keyboard_markup.add(*(types.KeyboardButton(text) for text in btns_text))


@dp.message_handler(commands='start')
async def start(message: types.Message):
    # Começa a conversa e pede o input do usuário
    await message.answer("Oi! Meu nome é Curious Bot. Vou manter uma com você. Por que você não me conta algo sobre você?", reply_markup=keyboard_markup)


@dp.message_handler(text=['Idade', 'Cor favorita', 'Número de irmãos'])
async def regular_choice(message: types.Message):
    print("== Usuário escolheu: 'Idade', 'Cor favorita', 'Número de irmãos' ==")
    # Pergunta ao usuário informações sobre a caregoria escolhida
    mensagem = message.text.capitalize()
    res.append(mensagem)
    #print(f'res::{res} e seu tamanho: {len(res)}')

    if mensagem in ['Idade', 'Cor favorita']:
        await message.reply(f'Sua {mensagem.lower()}? Sim, eu adoraria ouvir sobre isso!')
    else:
        await message.reply(f'{mensagem.capitalize()}? Sim, eu adoraria ouvir sobre isso!')


@dp.message_handler(text='Outra coisa...')
async def custom_choice(message: types.Message):
    print('== Usuário escolheu: Outra coisa... ==')
    # Peça ao usuário uma descrição de uma categoria personalizada
    await message.reply('Tudo bem, por favor me envie a categoria primeiro, por exemplo "habilidade mais impressionante"', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(text='Feito')
async def done(message: types.Message):
    await facts_to_str(res)
    # Formata as informeções para mandar para a mensagem
    msg = "\n".join(dados).join(['\n', '\n'])
    await message.answer(f'Aprendi estes fatos sobre você:\n{msg}Até a próxima!')


@dp.message_handler()
async def received_information(message: types.Message):
    user_data = message.text.capitalize()
    res.append(user_data)

    if len(res) == 1:
        res.remove(res[0])
        await asyncio.gather(asyncio.create_task(regular_choice(message)))
    if len(res) == 2:
        await facts_to_str(res)
        # Formata as informeções para mandar para a mensagem
        msg = "\n".join(dados).join(['\n', '\n'])
        await message.reply(f'''Legal! Só para você saber, isso é o que você já me disse:\n{msg}\nVocê pode me contar mais ou mudar sua opinião em algo.''', reply_markup=keyboard_markup)

if __name__ == '__main__':
    print('== RODANDO ==')
    executor.start_polling(dp, skip_updates=True)
