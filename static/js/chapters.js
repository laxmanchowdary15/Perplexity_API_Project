const chaptersBySubject = {
  "Maths": [
    "Real Numbers",
    "Polynomials",
    "Pair of Linear Equations in Two Variables",
    "Quadratic Equations",
    "Arithmetic Progressions",
    "Triangles",
    "Coordinate Geometry",
    "Introduction to Trigonometry",
    "Some Applications of Trigonometry",
    "Circles",
    "Constructions",
    "Areas Related to Circles",
    "Surface Areas and Volumes",
    "Statistics",
    "Probability"
  ],
  "Science": [
    "Heat",
    "Acids, Bases and Salts",
    "Refraction of Light at Plane Surfaces",
    "Refraction of Light at Curved Surfaces",
    "Human Eye and Colourful World",
    "Structure of Atom",
    "Classification of Elements - The Periodic Table",
    "Electric Current",
    "Electromagnetism",
    "Principles of Metallurgy",
    "Carbon and its Compounds",
    "Nutrition – Food Supplying System",
    "Respiration – The Energy Producing System",
    "Transportation – The Circulatory System",
    "Excretion – The Waste Disposal System",
    "Coordination – The Linking System",
    "Reproduction – The Generating System",
    "Coordination in Life Processes",
    "Our Environment – Our Concern",
    "Natural Resources"
  ],
  "Social": [
    "India: Relief Features",
    "Ideas of Development",
    "Production and Employment",
    "Climate of India",
    "Indian Rivers and Water Resources",
    "The People",
    "People and Settlement",
    "People and Migration",
    "Rampur: A Village Economy",
    "Globalisation",
    "Food Security",
    "Sustainable Development with Equity",
    "The World Between Wars 1900-1950: Part I",
    "The World Between Wars 1900-1950: Part II",
    "National Liberation Movements in the Colonies",
    "National Movement in India – Partition & Independence",
    "The Making of Independent India’s Constitution",
    "Independent India (The First 30 years – 1947-77)",
    "Emerging Political Trends 1977 to 2000",
    "Post-War World and India",
    "Social Movements in Our Times",
    "Citizens and the Governments"
  ],
  "English": [
    "A Letter to God",
    "Nelson Mandela: Long Walk to Freedom",
    "Two Stories about Flying and Black Aeroplane",
    "From the Diary of Anne Frank",
    "Glimpses of India (A Baker from Goa, Coorg, Tea from Assam)",
    "Mijbil the Otter",
    "Madam Rides the Bus",
    "The Sermon at Benares",
    "The Proposal",
    "Dust of Snow",
    "Fire and Ice",
    "A Tiger in the Zoo",
    "How to Tell Wild Animals",
    "The Ball Poem",
    "Amanda",
    "The Trees",
    "Fog",
    "The Tale of Custard the Dragon",
    "For Anne Gregory"
  ]
};

document.addEventListener('DOMContentLoaded', () => {
  const subjectSelect = document.getElementById('subject');
  const chapterSelect = document.getElementById('chapter');
  const form = document.querySelector('form');

  subjectSelect.addEventListener('change', () => {
    const selectedSubject = subjectSelect.value;
    const chapters = chaptersBySubject[selectedSubject] || [];

    chapterSelect.innerHTML = '<option value="" disabled selected>Select Chapter</option>';
    chapters.forEach(chapter => {
      const option = document.createElement('option');
      option.value = chapter;
      option.textContent = chapter;
      chapterSelect.appendChild(option);
    });
  });

  // Create download popup div
  const popup = document.createElement('div');
  popup.id = 'download-popup';
  popup.style.position = 'fixed';
  popup.style.bottom = '20px';
  popup.style.left = '50%';
  popup.style.transform = 'translateX(-50%)';
  popup.style.background = 'rgba(0,0,0,0.75)';
  popup.style.color = 'white';
  popup.style.padding = '15px 25px';
  popup.style.borderRadius = '8px';
  popup.style.fontSize = '1.2rem';
  popup.style.zIndex = '9999';
  popup.style.opacity = '0';
  popup.style.pointerEvents = 'none';
  popup.style.transition = 'opacity 0.5s ease';
  document.body.appendChild(popup);

  // Show popup with filename after form submit
  form.addEventListener('submit', (event) => {
    // Get selected subject and chapter for filename
    const subject = subjectSelect.value;
    const chapter = chapterSelect.value;
    const fileName = `${subject}_${chapter}_model_paper.pdf`;

    // Delay showing popup so it doesn’t flash too early
    setTimeout(() => {
      popup.textContent = `Download started: ${fileName}`;
      popup.classList.add('show');
      popup.style.opacity = '1';
      popup.style.pointerEvents = 'auto';

      setTimeout(() => {
        popup.style.opacity = '0';
        popup.style.pointerEvents = 'none';
      }, 3500);
    }, 1000); // 1 second delay
  });
});
