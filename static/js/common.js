bodyElem = document.getElementsByTagName('body')[0]

if (!localStorage.getItem('mdui-theme')) {
	bodyElem.classList.forEach(function (klass) {
		if (klass.startsWith('mdui-theme-layout-'))
			localStorage.setItem('mdui-theme', klass.slice(18))
	})
}

if (!localStorage.getItem('mdui-color')) {
	bodyElem.classList.forEach(function (klass) {
		if (klass.startsWith('mdui-theme-primary-'))
			localStorage.setItem('mdui-color', klass.slice(19))
	})
}

if (!localStorage.getItem('mikuinvidious_quality'))
	localStorage.setItem('mikuinvidious_quality', '32')

document.querySelectorAll('.js-only').forEach(x => x.classList.toggle('mdui-hidden'))
document.querySelectorAll('.nojs-only').forEach(x => x.classList.add('mdui-hidden'))

window.qnc = function (mikuinvidious_quality) {
	document.querySelector(`[href="javascript:qnc(${localStorage.getItem('mikuinvidious_quality')});"]`)
			.classList.remove('mdui-color-theme')

	localStorage.setItem('mikuinvidious_quality', mikuinvidious_quality)

	document.querySelector(`[href="javascript:qnc(${mikuinvidious_quality});"]`)
			.classList.add('mdui-color-theme')
}

bodyElem.className = `mdui-theme-layout-${localStorage.getItem('mdui-theme')}`
	+ ` mdui-theme-primary-${localStorage.getItem('mdui-color')}`
	+ ` mdui-theme-accent-${localStorage.getItem('mdui-color')}`

window.addEventListener('load', function() {
	document.querySelector(`[value="${localStorage.getItem('mdui-color')}"]`)
			.setAttribute('checked', '')
	document.querySelector(`[value="${localStorage.getItem('mdui-theme')}"]`)
			.setAttribute('checked', '')

	tf = document.getElementById('theme-sel')
	for (let inpa of tf['elements']['theme-layout']) {
		inpa.onclick = function () {
			newTheme = tf['elements']['theme-layout'].value

			bodyElem.classList.remove(`mdui-theme-layout-${localStorage.getItem('mdui-theme')}`)
			bodyElem.classList.add(`mdui-theme-layout-${newTheme}`)

			localStorage.setItem('mdui-theme', newTheme)
		}
	}

	cf = document.getElementById('color-sel')
	for (let inpa of cf['elements']['theme-primary']) {
		inpa.onclick = function () {
			newColor = cf['elements']['theme-primary'].value

			bodyElem.classList.remove(`mdui-theme-accent-${localStorage.getItem('mdui-color')}`)
			bodyElem.classList.remove(`mdui-theme-primary-${localStorage.getItem('mdui-color')}`)
			bodyElem.classList.add(`mdui-theme-accent-${newColor}`)
			bodyElem.classList.add(`mdui-theme-primary-${newColor}`)

			localStorage.setItem('mdui-color', newColor)
		}
	}

	document.querySelector(`[href="javascript:qnc(${localStorage.getItem('mikuinvidious_quality')});"]`)
			.classList.add('mdui-color-theme')
}, false)
