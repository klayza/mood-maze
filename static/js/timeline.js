// static/js/timeline.js
document.addEventListener('DOMContentLoaded', function () {
	// Get DOM elements
	const daysContainer = document.getElementById('days-container')
	const weekDropdown = document.getElementById('week-dropdown')
	const prevWeekBtn = document.getElementById('prev-week')
	const nextWeekBtn = document.getElementById('next-week')
	const modal = document.getElementById('entry-modal')
	const modalDate = document.getElementById('modal-date')
	const modalEntries = document.getElementById('modal-entries')
	const closeBtn = document.querySelector('.close')

	// Current date info
	const now = new Date()
	let currentYear = now.getFullYear()
	let currentWeek = getWeekNumber(now)

	// Populate week dropdown
	populateWeekDropdown()

	// Load initial week data
	loadWeekData(currentYear, currentWeek)

	// Event listeners
	weekDropdown.addEventListener('change', function () {
		const [year, week] = this.value.split('-W')
		currentYear = parseInt(year)
		currentWeek = parseInt(week)
		loadWeekData(currentYear, currentWeek)
	})

	prevWeekBtn.addEventListener('click', function () {
		navigateWeek(-1)
	})

	nextWeekBtn.addEventListener('click', function () {
		navigateWeek(1)
	})

	closeBtn.addEventListener('click', function () {
		modal.style.display = 'none'
	})

	window.addEventListener('click', function (event) {
		if (event.target === modal) {
			modal.style.display = 'none'
		}
	})

	// Functions
	function getWeekNumber(date) {
		const d = new Date(date)
		d.setHours(0, 0, 0, 0)
		d.setDate(d.getDate() + 3 - ((d.getDay() + 6) % 7))
		const week1 = new Date(d.getFullYear(), 0, 4)
		return 1 + Math.round(((d - week1) / 86400000 - 3 + ((week1.getDay() + 6) % 7)) / 7)
	}

	function populateWeekDropdown() {
		// Get last 12 weeks and next 4 weeks
		const options = []
		const currentDate = new Date()

		for (let i = -12; i <= 4; i++) {
			const date = new Date(currentDate)
			date.setDate(date.getDate() + i * 7)

			const year = date.getFullYear()
			const week = getWeekNumber(date)
			const startDate = getDateOfWeek(year, week, 1) // Monday
			const endDate = getDateOfWeek(year, week, 0) // Sunday

			const option = {
				value: `${year}-W${week}`,
				text: `Week ${week}: ${formatDate(startDate)} - ${formatDate(endDate)}`,
			}

			options.push(option)
		}

		// Add options to dropdown
		// static/js/timeline.js (continued)
		// Add options to dropdown
		weekDropdown.innerHTML = ''
		options.forEach((option) => {
			const optionElement = document.createElement('option')
			optionElement.value = option.value
			optionElement.textContent = option.text

			// Select current week
			if (option.value === `${currentYear}-W${currentWeek}`) {
				optionElement.selected = true
			}

			weekDropdown.appendChild(optionElement)
		})
	}

	function getDateOfWeek(year, week, dayOfWeek) {
		// dayOfWeek: 0 = Sunday, 1 = Monday, etc.
		const firstDayOfYear = new Date(year, 0, 1)
		const daysOffset = (dayOfWeek - firstDayOfYear.getDay() + 7) % 7

		// Find the first day of the week
		const firstWeekDay = new Date(year, 0, 1 + daysOffset)

		// Add (week - 1) * 7 days to get to the requested week
		const targetDate = new Date(firstWeekDay)
		targetDate.setDate(firstWeekDay.getDate() + (week - 1) * 7)

		return targetDate
	}

	function formatDate(date) {
		const options = { month: 'short', day: 'numeric' }
		return date.toLocaleDateString('en-US', options)
	}

	function navigateWeek(offset) {
		// Create a date for the current week
		const date = getDateOfWeek(currentYear, currentWeek, 1)

		// Add/subtract 7 days
		date.setDate(date.getDate() + offset * 7)

		// Update current year and week
		currentYear = date.getFullYear()
		currentWeek = getWeekNumber(date)

		// Update dropdown selection
		weekDropdown.value = `${currentYear}-W${currentWeek}`

		// Load new week data
		loadWeekData(currentYear, currentWeek)
	}

	function loadWeekData(year, week) {
		fetch(`/api/week_data?year=${year}&week=${week}`)
			.then((response) => response.json())
			.then((data) => {
				renderWeek(data)
			})
			.catch((error) => {
				console.error('Error loading week data:', error)
			})
	}

	function renderWeek(weekData) {
		daysContainer.innerHTML = ''

		// Get dates for the week
		const startDate = new Date(weekData.start_date)

		// Create day cards for each day of the week
		for (let i = 0; i < 7; i++) {
			const date = new Date(startDate)
			date.setDate(startDate.getDate() + i)

			const dateStr = date.toISOString().split('T')[0]
			const dayData = weekData.days[dateStr] || {
				date: dateStr,
				emotion: 'neutral',
				score: 0,
				entries: [],
			}

			// Create day card
			const dayCard = document.createElement('div')
			dayCard.className = 'day-card'
			dayCard.style.backgroundColor = getEmotionLightColor(dayData.emotion)

			// Format date
			const dayNames = [
				'Sunday',
				'Monday',
				'Tuesday',
				'Wednesday',
				'Thursday',
				'Friday',
				'Saturday',
			]
			const dayName = dayNames[date.getDay()]
			const formattedDate = formatDate(date)

			dayCard.innerHTML = `
                <div class="day-name">${dayName}</div>
                <div class="day-date">${formattedDate}</div>
                <div class="day-emotion emotion-${dayData.emotion.toLowerCase()}">${
				dayData.emotion
			}</div>
            `

			// Add click event to show entries
			dayCard.addEventListener('click', function () {
				showDayEntries(dayData, `${dayName}, ${date.toLocaleDateString()}`)
			})

			daysContainer.appendChild(dayCard)
		}
	}

	function getEmotionLightColor(emotion) {
		// Return lighter version of emotion colors for background
		const colors = {
			joy: '#fff9c4',
			love: '#fce4ec',
			anger: '#ffebee',
			sadness: '#e3f2fd',
			fear: '#f3e5f5',
			surprise: '#e0f7fa',
			disgust: '#f1f8e9',
			neutral: '#f5f5f5',
			admiration: '#f3e5f5',
			amusement: '#fff3e0',
			annoyance: '#fbe9e7',
			approval: '#e8f5e9',
			caring: '#fce4ec',
			confusion: '#ede7f6',
			curiosity: '#e8eaf6',
			desire: '#fce4ec',
			disappointment: '#efebe9',
			disapproval: '#ffebee',
			embarrassment: '#fbe9e7',
			excitement: '#fffde7',
			gratitude: '#f1f8e9',
			grief: '#eceff1',
			nervousness: '#f9fbe7',
			optimism: '#fff8e1',
			pride: '#ffebee',
			realization: '#e0f7fa',
			relief: '#e0f7fa',
			remorse: '#eceff1',
		}

		return colors[emotion.toLowerCase()] || '#f5f5f5'
	}

	function showDayEntries(dayData, dateLabel) {
		// Set modal title
		modalDate.textContent = dateLabel

		// Clear previous entries
		modalEntries.innerHTML = ''

		if (dayData.entries.length === 0) {
			modalEntries.innerHTML = '<p>No entries for this day.</p>'
		} else {
			// Create entry cards
			dayData.entries.forEach((entry) => {
				const entryCard = document.createElement('div')
				entryCard.className = 'entry-card'

				// Create time element
				const timeEl = document.createElement('div')
				timeEl.className = 'entry-time'
				timeEl.textContent = entry.time

				// Create sentences with emotion highlights
				const sentencesContainer = document.createElement('div')
				sentencesContainer.className = 'entry-sentences'

				entry.analysis.sentences.forEach((sentence) => {
					const sentenceEl = document.createElement('div')
					sentenceEl.className = `sentence emotion-${sentence.emotion.toLowerCase()}`
					sentenceEl.textContent = sentence.text
					sentencesContainer.appendChild(sentenceEl)
				})

				// Create tags container
				const tagsContainer = document.createElement('div')
				tagsContainer.className = 'entry-tags'

				if (entry.tags && entry.tags.length > 0) {
					entry.tags.forEach((tag) => {
						const tagEl = document.createElement('span')
						tagEl.className = 'tag'
						tagEl.textContent = tag
						tagsContainer.appendChild(tagEl)
					})
				}

				// Append all elements to entry card
				entryCard.appendChild(timeEl)
				entryCard.appendChild(sentencesContainer)
				entryCard.appendChild(tagsContainer)

				modalEntries.appendChild(entryCard)
			})
		}

		// Show modal
		modal.style.display = 'block'
	}
})
