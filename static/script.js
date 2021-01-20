var getelem = id => document.getElementById(id)
var copyToClipboard = text => {
    var temp = document.createElement('input')
    document.body.appendChild(temp)
    temp.value = text
    temp.select()
    document.execCommand('copy')
    document.body.removeChild(temp)
}
window.addEventListener('load', async () => {
    var path = location.pathname
    if (path == '/') {
        var data = JSON.parse(await (await fetch('/api')).text())
        var urls = getelem('urls')
        data.forEach(t => {
            var e = document.createElement('a')
            e.href = `/${t}`
            e.innerHTML = t
            urls.appendChild(e)
            urls.appendChild(document.createElement('br'))
        })
    } else {
        var t = path.split('/')[1]
        var typesdata = JSON.parse(await (await fetch('/api')).text())
        var data = JSON.parse(await (await fetch(`/api/${t}`)).text())
        var menu = getelem('menu')
        var items = getelem('items')
        if (data.status == 404) {location.href = '/'}
        typesdata.forEach(t => {
            var e = document.createElement('a')
            e.href = `/${t}`
            e.innerHTML = t
            menu.appendChild(e)
            var s = document.createElement('span')
            s.innerHTML = ' '
            menu.appendChild(s)
        })
        var e = document.createElement('a')
        e.href = '/'
        e.innerHTML = 'back'
        menu.appendChild(e)

        data.forEach(item => {
            var tr = document.createElement('tr')
            var image = document.createElement('th')
            image.style.backgroundImage = `url(static/${item.rarity ? item.rarity : 'uncommon'}.png)`
            image.style.backgroundSize = 'cover'
            var img = document.createElement('img')
            img.src = item.images.smallIcon ? item.images.smallIcon.url ? item.images.smallIcon.url : item.images.smallIcon : item.images.icon.url ? item.images.icon.url : item.images.icon
            img.style.border = '0'
            img.width = '128'
            img.height = '128'
            image.appendChild(img)
            tr.appendChild(image)

            var id = document.createElement('th')
            var idspan = document.createElement('span')
            idspan.innerHTML = item.id
            id.appendChild(idspan)
            id.appendChild(document.createElement('br'))
            id.appendChild(document.createElement('br'))
            var copybutton = document.createElement('button')
            copybutton.innerHTML = 'Copy ID'
            copybutton.addEventListener('click', () => {
                copyToClipboard(item.id)
            })
            id.appendChild(copybutton)
            tr.appendChild(id)

            var idlength = document.createElement('th')
            var idlen = document.createElement('span')
            idlen.innerHTML = item.id.length
            idlength.appendChild(idlen)
            tr.appendChild(idlength)

            var name = document.createElement('th')
            var namespan = document.createElement('span')
            namespan.innerHTML = t != 'banners' ? item.name : item.devName
            name.appendChild(namespan)
            tr.appendChild(name)

            var description = document.createElement('th')
            var descriptionspan = document.createElement('span')
            descriptionspan.innerHTML = item.description
            description.appendChild(descriptionspan)
            tr.appendChild(description)

            items.appendChild(tr)
        })
    }
})