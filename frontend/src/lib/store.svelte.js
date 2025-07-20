import { browser } from '$app/environment';
import { page } from '$app/state';
import { invalidate } from '$app/navigation';


export let user = $state({ value: null });

export let module = $state({
	module: null,
	value: {},
	open(module, value = {}) {
		this.module = module
		this.value = value
	},
	close() {
		this.module = null;
		this.value = {};
	}
});

export let loading = $state({
	value: null,
	open(message = 'Loading . . .') {
		this.value = message
	},
	close() {
		this.value = null;
	}
});


export let notify = $state({
	value: [],
	open(message, status = 200) {
		this.value.push({
			message,
			status,
			key: () => {
				const chars = '0123456789abcdef';
				let code = '#';

				for (let i = 0; i < 10; i++) {
					code += chars[Math.floor(Math.random() * chars.length)];
				}
				return code;
			}
		});
	},
	close(key) {
		this.value = this.value.filter((x) => x.key != key);
	}
});


export const token = {
	name: 'token',

	get value() {
		let cookies = document.cookie.split(';');
		for (let i in cookies) {
			let temp = cookies[i].split('=');
			if (temp[0].trim() === this.name) {
				return temp[1];
			}
		}
		return '';
	},

	set value(v) {
		let day = v ? 1 : -10000;
		let date = new Date();
		date.setTime(date.getTime() + day * 24 * 60 * 60 * 1000);
		if (browser) {
			document.cookie = `${this.name}=${v};expires=${date.toUTCString()};path=/`;
		}
	}
};



export const page_state = $state({
	searchParams: {},

	set(key, val) {
		this.searchParams[key] = val
		if (!val) {
			delete this.searchParams[key];
		}
		if (key != "page_no") {
			delete this.searchParams["page_no"];
		}

		let ss = new URLSearchParams(this.searchParams);

		page.url.search = ss.toString();
		window.history.replaceState(history.state, '', page.url.href);
		window.scrollTo({ top: 0, behavior: 'smooth' });


		loading.open()
		invalidate(() => true);
	}


})
