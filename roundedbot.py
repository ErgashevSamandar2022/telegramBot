from aiogram import Bot,Dispatcher,types,F
import asyncio
from aiogram.filters import Command
from aiogram import html
from moviepy.editor import *
import os
import PIL
PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
tokenAPI='7041422228:AAFT3WNZGuFimkhLZeMdA7jpfePZOjr6Rjo'
bot=Bot(token=tokenAPI,parse_mode='HTML')
dp=Dispatcher()


@dp.message(Command('start'))
async def start(message:types.Message):
    await message.answer(f'Welcome, <b>{message.chat.first_name} {message.chat.last_name if message.chat.last_name!=None else ""}</b> ',protect_content=True)

@dp.message(F.video)
async def get_msg(message:types.Message):
   video_file = message.video
   file_id = video_file.file_id
   file_uniqueId = video_file.file_unique_id
   file_size = video_file.file_size/(1024*1024)
   file_name = video_file.file_name
   duration = video_file.duration
   if duration > 60:
     await message.answer('Iltimis video davimiyligi 60 sekund dan kam bolsin')
   else:
     if file_size > 10:
       await message.answer('Video hajmi 10 MB dan kichik bolsin')
     else:
       file = await bot.get_file(file_id=file_id)
       custom_file = f'{file_uniqueId}.mp4'
       await bot.download(file=file,destination=custom_file)
      #  await message.answer('video yuklab olindi')
       clip = VideoFileClip(filename = custom_file)
       video = clip.resize((640,640))
       custom_file2=f'{file_name}.mp4'
       video.write_videofile(custom_file2,codec = 'libx264')
       sending_file = types.input_file.FSInputFile(path=custom_file2,filename=file_name)
       await bot.send_chat_action(chat_id=message.from_user.id,action = 'upload_video')
       await message.answer_video_note(video_note=sending_file)
       try:
         if os.path.isfile(custom_file2):
           os.remove(custom_file2)
         if os.path.isfile(custom_file):
           os.remove(custom_file)
       except:
      		pass
      	
async def main():
    await dp.start_polling(bot)

if __name__=='__main__':
    asyncio.run(main())