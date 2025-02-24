document.addEventListener('DOMContentLoaded', () => {
	const form = document.getElementById('audioForm');
	const resultDiv = document.getElementById('result');

	form.addEventListener('submit', async (e) => {
			e.preventDefault();

			// Собираем данные из формы
			const formData = new FormData(form);
			const data = {
					prompt: formData.get('prompt'),
					style: formData.get('style') || null,
					title: formData.get('title') || null,
					customMode: formData.get('customMode') === 'true',
					instrumental: formData.get('instrumental') === 'true',
					model: formData.get('model'),
					callbackUrl: formData.get('callbackUrl')
			};

			try {
					const response = await fetch('/generate-audio', {
							method: 'POST',
							headers: {
									'Content-Type': 'application/json',
							},
							body: JSON.stringify(data)
					});

					if (!response.ok) {
							throw new Error(`HTTP error! status: ${response.status}`);
					}

					const result = await response.json();
					resultDiv.innerHTML = `<pre>${JSON.stringify(result, null, 2)}</pre>`;
			} catch (error) {
					resultDiv.innerHTML = `<p>Ошибка: ${error.message}</p>`;
			}
	});
});