import discord
from discord.ext import commands
from model import get_class
import random,os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hi(ctx):
    await ctx.send(f'Halo!! bot sudah siap, nama ku {bot.user}!')
    await ctx.send(f'Jika bingung, gunakan command $help_ untuk melihat command list')

@bot.command()
async def coin_flip(ctx):
    p = random.randint(1,10)
    if p <= 5 :
        await ctx.send('Tails!!')

    else :
        await ctx.send('Head!!')

@bot.command()
async def clasify(ctx):
    # kode untuk bot menerima gambar
    if ctx.message.attachments: 
        for file in ctx.message.attachments: 
            file_name = file.filename 
            file_url = file.url
            await file.save(f'./{file_name}')
            hasil, skor = get_class('keras_model.h5', 'labels.txt', f'./{file.filename}')
            
            # kode untuk memproses gambar (ubah dengan melihat labels.txt)
            #INFERENSI
            if hasil == 'Sampah plastik' and skor >= 0.65:
                await ctx.send('\nGambar terdeteksi sebagai sampah Plastik!')
                await ctx.send('\nKategori : Anorganik')
                await ctx.send('\nDampak buruk : \n- Sulit terurai ratusan tahun\n- Menyumbat saluran air → banjir \n- Mencemari laut, berbahaya bagi hewan \n- Melepaskan zat beracun jika dibakar')
                await ctx.send('\nCara mengurangi dampak buruk : \n- Kurangi plastik sekali pakai \n- Gunakan tas kain/botol isi ulang \n- Daur ulang jadi barang baru \n- Terapkan 3R (Reduce, Reuse, Recycle)')
                await ctx.send('=========================================================')

            elif hasil == 'Sampah kaleng' and skor >= 0.65:
                await ctx.send('\nGambar terdeteksi sebagai sampah Kaleng!')
                await ctx.send('\nKategori : Anorganik')
                await ctx.send('\nDampak buruk : \n- Berkarat → mencemari tanah \n- Dibakar menimbulkan polusi udara \n- Bisa melukai jika dibuang sembarangan')
                await ctx.send('\nCara mengurangi dampak buruk : \n- Kumpulkan dan jual ke pengepul/daur ulang logam \n- Manfaatkan jadi kerajinan/pot \n- Kurangi konsumsi produk kemasan kaleng')
                await ctx.send('=========================================================')
            elif hasil == 'Sampah kaca' and skor >= 0.65 :
                await ctx.send('\nGambar terdeteksi sebagai sampah Kaca!')
                await ctx.send('\nKategori : Anorganik')
                await ctx.send('\nDampak buruk : \n- Pecahan kaca dapat melukai manusia/hewan \n- Sulit terurai \n- Menumpuk jadi limbah yang merusak pemandangan')
                await ctx.send('\nCara mengurangi dampak buruk :\n- Gunakan ulang wadah kaca \n- Daur ulang jadi botol/bahan bangunan \n- Kumpulkan pecahan dengan aman \n- Kurangi beli kemasan kaca sekali pakai')
                await ctx.send('=========================================================')
            elif hasil == 'Sisa makanan' and skor >= 0.65:
                await ctx.send('\nGambar terdeteksi sebagai Sisa makanan!')
                await ctx.send('\nKategori : Organik')
                await ctx.send('\nDampak buruk : \n- Menimbulkan bau busuk \n- Mengundang hama (lalat, tikus) \n- Menghasilkan gas metana (pemanasan global) \n- Mencemari tanah/air jika menumpuk di TPA')
                await ctx.send('\nCara mengurangi dampak buruk : \n- Olah jadi kompos/pupuk cair \n- Manfaatkan untuk pakan ternak \n- Kurangi pemborosan makanan \n- Gunakan biogas dari limbah organik')
                await ctx.send('=========================================================')
            else:
                await ctx.send('GAMBAR MU KEMUNGKINAN: salah format/blur/corrupt')
                await ctx.send('KIRIM GAMBAR BARU!!!')
    else:
        await ctx.send('KAMU TIDAK MENGIRIM APA APA!!')



@bot.command()
async def help_(ctx):
    command_list = {
        '$hi' : "menyapa bot",
        '$clasify' : 'klasifikasi gambar sampah',
        '$coin_flip' : 'coin_flip',
        '$exam' : 'ujian / minigame'
    }

    await ctx.send('Command yang bisa kamu gunakan :')
    for i in command_list.keys():
        await ctx.send(f'{i} : {command_list[i]}')


user_answer = {}
@bot.command()
async def exam(ctx):
    base_folder = 'Exam'
    all_files = []

    # Cari subfolder kategori
    for root, dirs, files in os.walk(base_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                full_path = os.path.join(root, file)
                category = os.path.basename(root)  # Nama folder induk -> kategori
                all_files.append((full_path, category))

    if not all_files:
        await ctx.send("Maaf, tidak ada file soal yang tersedia.")
        return

    # Pilih gambar random + kategori
    chosen_file, correct_category = random.choice(all_files)

    with open(chosen_file, 'rb') as f:
        picture = discord.File(f)

    # Kirim soal
    await ctx.send(file=picture)
    await ctx.send(
        "Gambar diatas adalah sampah...\n"
        "A. Kaca\nB. Plastik\nC. Sisa makanan\nD. Kaleng"
    )

    # Mapping jawaban user -> kategori
    options = {
        "A": "Kaca",
        "B": "Plastik",
        "C": "Sisa makanan",
        "D": "Kaleng"
    }

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.upper() in options

    try:
        msg = await bot.wait_for('message', check=check, timeout=30.0)
        user_choice = msg.content.upper()
        user_answer[ctx.author.id] = options[user_choice]

        if options[user_choice] == correct_category:
            await ctx.send(f"✅ Benar! Itu adalah {correct_category}.")
        else:
            await ctx.send(f"❌ Salah. Jawaban yang benar adalah **{correct_category}**.")

    except:
        await ctx.send('⏰ Waktumu Habis!!')



bot.run("MTQxNTY4NDQ2NjEzOTIwNTcxMw.GfW_F2.nAvrT32a7r6Pt4-J0tyhADglfV2Iq5QHfy6nIA")
#MTQxNTY4NDQ2NjEzOTIwNTcxMw.GfW_F2.nAvrT32a7r6Pt4-J0tyhADglfV2Iq5QHfy6nIA
