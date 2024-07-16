<script>
	function generatePDF() {
		// Choose the element that your content will be rendered to.
		const element = document.getElementById('invoice');
		// Choose the element and save the PDF for your user.
		html2pdf().from(element).save();
	}
</script>

<svelte:head>
	<script
		src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"
		integrity="sha512-GsLlZN/3F2ErC5ifS5QtgpiJtWd43JWSuIgh7mbzZ8zBps+dvLusV+eNQATqgA/HdeKFVgA5v3S/cIrLF7QnIg=="
		crossorigin="anonymous"
		referrerpolicy="no-referrer"
	></script>
</svelte:head>

<div id="invoice">hello</div>
<button on:click={generatePDF}>print</button>

<style>
	* {
		-webkit-print-color-adjust: exact !important;
		print-color-adjust: exact !important;

		font-size: 0.6rem;
	}

	@media print {
		#invoice {
			width: 400px;
		}
	}
</style>
