const PROXY_URL = '/proxy/vid/'
let player = document.getElementById('video-player')
let qntext = document.getElementById('quality-text')
let autonext = document.getElementById('autonext-check')
let playerSource = document.getElementById('video-source')

function switch_qn (qn) {
	currentTime = player.currentTime
	paused = player.paused

	playerSource.src = PROXY_URL + srcinfo[qn]['durl'][0]['url']
	player.load()

	player.currentTime = currentTime
	if (!paused) player.play()

	let desc = '未知画质'
	for (const qf of srcinfo[qn]['support_formats']) {
		if (qf['quality'] == qn) {
			desc = qf['new_description']
			break
		}
	}

	qntext.innerText = desc
	mdui.snackbar({ message: `已切换至${desc}` })
}

player.onended = function (e) {
	if (localStorage.getItem('autonext') != 'yes')
		return

	recums = document.querySelectorAll('.mdui-card-actions > a')
	if (recums.length == 0) {
		mdui.snackbar({ 'message': '没有更多视频可以播放啦' })
	} else {
		mdui.snackbar({ 'message': '三秒后将跳转到下一个视频' })
		setTimeout(function () {
			localStorage.setItem('autonext-play', 'yes')
			window.location = recums[0].href
		}, 3000)
	}
}

window.addEventListener('load', function() {
	qn = Number(localStorage.getItem('quality'))
	if (!(qn in srcinfo)) {
		realqn = 0
		for (let availqn of Object.keys(srcinfo)) {
			if (availqn > qn)
				break
			realqn = availqn
		}
		qn = realqn ? realqn : Object.keys(srcinfo)[0]
	}

	console.log(qn)
	playerSource.src = PROXY_URL + srcinfo[qn]['durl'][0]['url']
	player.load()

	let desc = '未知画质'
	for (const qf of srcinfo[qn]['support_formats']) {
		if (qf['quality'] == qn) {
			desc = qf['new_description']
			break
		}
	}
	qntext.innerText = desc

	if (localStorage.getItem('autonext') == 'yes') {
		autonext.checked = true

		if (localStorage.getItem('autonext-play') == 'yes') {
			localStorage.setItem('autonext-play', 'no')
			player.play()
		}
	}
}, false)