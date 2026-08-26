import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update body
html = html.replace(
    '<body class="bg-brand-bg text-gray-800 font-sans h-screen overflow-hidden flex flex-col text-sm">',
    '<body class="bg-brand-bg text-gray-800 font-sans h-screen overflow-hidden flex flex-col text-sm max-md:bg-[#0f0f0f] max-md:text-[#e8eaed]">'
)

# 2. Hide desktop header on mobile
html = html.replace(
    '<header class="flex items-center justify-between px-4 h-16 bg-brand-bg shrink-0">',
    '<header class="hidden md:flex items-center justify-between px-4 h-16 bg-brand-bg shrink-0">'
)

# 3. Handle Slim Sidebar / Mobile Bottom Nav
slim_sidebar_find = '<div class="w-[72px] flex flex-col items-center py-4 bg-brand-bg shrink-0 gap-4">'
slim_sidebar_replace = '''
        <!-- Mobile Bottom Nav -->
        <div class="md:hidden fixed bottom-0 left-0 right-0 h-[64px] bg-[#1a1a1c] flex items-center justify-around z-50 shadow-[0_-4px_6px_rgba(0,0,0,0.3)]">
            <div class="flex flex-col items-center justify-center relative cursor-pointer group">
                <div class="px-5 py-1rounded-full bg-[#004a77] relative">
                    <span class="material-symbols-outlined icon-fill text-[#c2e7ff]">mail</span>
                    <div class="absolute -top-1 -right-2 bg-red-300 text-red-900 text-[10px] font-bold px-1.5 rounded-full border-2 border-[#004a77]">99+</div>
                </div>
            </div>
            <div class="flex flex-col items-center justify-center cursor-pointer text-[#9aa0a6]">
                <span class="material-symbols-outlined">videocam</span>
            </div>
        </div>
        
        <!-- Desktop Slim Sidebar -->
        <div class="hidden md:flex w-[72px] flex-col items-center py-4 bg-brand-bg shrink-0 gap-4">'''
html = html.replace(slim_sidebar_find, slim_sidebar_replace)

# 4. Hide desktop folders nav & right aside
html = html.replace(
    '<nav class="w-[256px] flex flex-col shrink-0 overflow-y-auto">',
    '<nav class="hidden md:flex w-[256px] flex-col shrink-0 overflow-y-auto">'
)
html = html.replace(
    '<aside class="w-14 flex flex-col items-center py-4 bg-brand-bg shrink-0 border-l border-transparent">',
    '<aside class="hidden xl:flex w-14 flex-col items-center py-4 bg-brand-bg shrink-0 border-l border-transparent">'
)

# 5. Update main tag and add Mobile Header inside main
main_find = '<main class="flex-1 bg-white rounded-t-2xl shadow-sm flex flex-col mr-4 overflow-hidden relative">'
main_replace = '''<main class="flex-1 bg-white max-md:bg-[#0f0f0f] md:rounded-t-2xl shadow-sm flex flex-col md:mr-4 overflow-hidden relative">

            <!-- Mobile Header & Title -->
            <div class="md:hidden px-4 pt-3 pb-1 shrink-0 z-10 bg-[#0f0f0f]">
                <div class="bg-[#1e1e1e] rounded-full h-[52px] flex items-center px-4 gap-4 shadow-[0_2px_4px_rgba(0,0,0,0.5)] mt-1">
                    <span class="material-symbols-outlined text-[#e8eaed] text-[24px]">menu</span>
                    <input type="text" placeholder="Buscar en el correo" class="bg-transparent border-none focus:ring-0 w-full outline-none text-[16px] text-white placeholder-[#9aa0a6] mt-0.5" />
                    <!-- User Avatar from image -->
                    <div class="w-8 h-8 rounded-full bg-[#1b3a57] border border-blue-500 overflow-hidden shrink-0 flex items-center justify-center relative cursor-pointer">
                        <img src="https://logodownload.org/wp-content/uploads/2021/03/usach-logo-2.png" alt="Avatar" class="h-10 w-10 object-cover opacity-50" onerror="this.style.display='none'">
                        <span class="text-[#c2e7ff] text-sm absolute">R</span>
                    </div>
                </div>
                <div class="mt-5 text-[12px] font-medium text-[#9aa0a6] tracking-wide px-2 mb-1">
                    Recibidos (todos)
                </div>
            </div>
            
            <!-- Mobile FAB -->
            <div class="md:hidden fixed bottom-[84px] right-4 bg-[#c2e7ff] hover:bg-[#a8d3f0] text-[#041e49] rounded-2xl px-5 py-4 flex items-center justify-center shadow-lg z-50 cursor-pointer gap-2 transition-colors">
                <span class="material-symbols-outlined icon-fill">edit</span>
                <span class="font-medium mr-1 text-sm">Redactar</span>
            </div>'''
html = html.replace(main_find, main_replace)

# 6. Hide desktop controls inside main
html = html.replace(
    '<div class="flex items-center justify-between px-4 h-12 border-b border-gray-100">',
    '<div class="hidden md:flex items-center justify-between px-4 h-12 border-b border-gray-100">'
)
html = html.replace(
    '<div class="m-4 border border-gray-200 rounded-2xl relative bg-white">',
    '<div class="hidden md:block m-4 border border-gray-200 rounded-2xl relative bg-white">'
)

# 7. Update emails wrapper
html = html.replace(
    '<div class="flex-1 overflow-y-auto bg-white">',
    '<div class="flex-1 overflow-y-auto bg-white max-md:bg-[#0f0f0f] max-md:pb-32">'
)

# 8. Function to patch each email row
def transform_email_row(match):
    row_html = match.group(0)
    # Give the outer div dark mode classes
    row_html = row_html.replace('bg-white', 'bg-white max-md:bg-[#0f0f0f]')
    row_html = row_html.replace('bg-[#f2f6fc]', 'bg-[#f2f6fc] max-md:bg-[#0f0f0f]')
    row_html = row_html.replace('border-gray-100', 'border-gray-100 max-md:border-none')
    
    # Hide desktop left star/checkbox
    row_html = row_html.replace('<div class="flex items-center gap-3 w-16 shrink-0">', '<div class="hidden md:flex items-center gap-3 w-16 shrink-0">')
    
    # Extract sender text for mobile avatar
    sender_match = re.search(r'<div class="w-\[180px\][^>]*>([^<]+)</div>', row_html)
    sender = sender_match.group(1).strip() if sender_match else "A"
    initial = sender[0] if sender else "A"
    
    # Replace sender div
    old_sender = sender_match.group(0)
    new_sender = f'<div class="md:w-[180px] font-bold text-gray-900 max-md:text-[#e8eaed] truncate shrink-0 max-md:text-[15px] max-md:mb-0.5">{sender}</div>'
    row_html = row_html.replace(old_sender, new_sender)
    
    # Inject mobile avatar + restructure flex
    # Before the old sender, we inject the mobile avatar container
    avatar_colors = {'D': 'bg-[#1b3a57] text-[#c2e7ff]', 'B': 'bg-[#0f5223] text-[#81c995]', 'V': 'bg-purple-900 text-purple-200', 's': 'bg-teal-900 text-teal-200', 'A': 'bg-red-900 text-red-200'}
    color = avatar_colors.get(initial, 'bg-[#3c4043] text-gray-300')
    
    avatar_html = f'<div class="hidden max-md:flex w-[40px] h-[40px] rounded-full {color} font-medium items-center justify-center text-xl shrink-0 mt-0.5">{initial}</div>'
    
    flex_content_start_1 = '<div class="flex-1 flex flex-col justify-center min-w-0 pr-8">'
    flex_content_start_2 = '<div class="flex-1 flex items-center text-sm truncate pr-8">'
    if flex_content_start_1 in row_html:
        row_html = row_html.replace(flex_content_start_1, '<div class="flex-1 flex flex-col justify-center min-w-0 md:flex-row md:items-center text-sm truncate md:pr-8">')
    elif flex_content_start_2 in row_html:
         row_html = row_html.replace(flex_content_start_2, '<div class="flex-1 flex flex-col justify-center min-w-0 md:flex-row md:items-center text-sm md:truncate md:pr-8">')
    
    row_html = row_html.replace('<div class="flex items-center px-4 py-2', '<div class="flex items-start md:items-center px-4 md:py-2 py-3 gap-4 md:gap-0')
    
    # Change specific text colors for dark mode
    row_html = row_html.replace('text-gray-900', 'text-gray-900 max-md:text-[#e8eaed]')
    row_html = row_html.replace('text-gray-500', 'text-gray-500 max-md:text-[#9aa0a6]')
    row_html = row_html.replace('text-gray-700', 'text-gray-700 max-md:text-[#e8eaed]') # Unread text
    
    # Right date & Desktop right-actions
    row_html = re.sub(r'<div class="w-16 (text-right[^>]+)>([^<]+)</div>', r'<div class="md:w-16 \1 max-md:absolute max-md:top-[14px] max-md:right-4 max-md:text-xs max-md:text-[#9aa0a6] max-md:group-hover:block">\2</div>', row_html)
    
    # Insert avatar right after the outer div starts for mobile
    # Replace the hidden left column with hidden left column + mobile avatar
    row_html = row_html.replace('<div class="hidden md:flex items-center gap-3 w-16 shrink-0">', f'{avatar_html}\n                    <div class="hidden md:flex items-center gap-3 w-16 shrink-0">')
    
    # Add trailing star for mobile
    star_html = '<span class="hidden max-md:block material-symbols-outlined absolute right-4 bottom-3 text-[#9aa0a6] text-[22px]">star_border</span>'
    row_html = row_html.replace('</div>\n                    <div class="absolute right-4', f'{star_html}\n                    </div>\n                    <div class="absolute right-4')

    return row_html

html = re.sub(r'<div\n\s*class="flex items-center px-4 py-2 border-b border-gray-100.*?<div class="absolute right-4[^>]*>.*?</div>\n\s*</div>', transform_email_row, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("done")
