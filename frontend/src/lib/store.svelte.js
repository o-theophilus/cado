import { browser } from '$app/environment';
import { page } from '$app/state';
import { invalidate } from '$app/navigation';
import { pushState, replaceState } from "$app/navigation"


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


export const state = $state()
export const set_state = (key, value) => {
	page.url.searchParams.set(key, value);

	if (value == '') {
		page.url.searchParams.delete(key);
	}
	if (key != "page_no") {
		page.url.searchParams.delete("page_no");
	}

	window.history.replaceState(history.state, '', page.url.href);
	window.scrollTo({ top: 0, behavior: 'smooth' });


	console.log(page.url.href);
	console.log(page.data.page_name);

	// let _state = state
	// let i = _state.findIndex(x => x.name == page.data.page_name)
	// _state[i].loaded = false
	// _state[i].search = page.url.search
	// state.set(_state)

	// loading.set("Loading . . .")
	// invalidate(() => true);
};

export const page_state = $state({
	value: {},

	set(key, value) {
		page.url.searchParams.set(key, value);

		if (value == '') {
			page.url.searchParams.delete(key);
		}
		if (key != "page_no") {
			page.url.searchParams.delete("page_no");
		}

		this.value[page.data.page_name] = {
			loaded: false,
			search: page.url.search,
		}



		console.log(page.url);
		// replaceState(history.state, page.url.search);
		window.history.replaceState(history.state, '', page.url.href);
		window.scrollTo({ top: 0, behavior: 'smooth' });





		// loading.open()
		invalidate(() => true);
	}


})
