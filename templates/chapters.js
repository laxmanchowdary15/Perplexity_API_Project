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
    "Chemical Reactions and Equations",
    "Acids, Bases and Salts",
    "Metals and Non-metals",
    "Carbon and Its Compounds",
    "Periodic Classification of Elements",
    "Life Processes",
    "Control and Coordination",
    "How do Organisms Reproduce?",
    "Heredity and Evolution",
    "Light – Reflection and Refraction",
    "The Human Eye and the Colourful World",
    "Electricity",
    "Magnetic Effects of Electric Current",
    "Sources of Energy"
  ],
  "Social": [
    "India and the Contemporary World – II",
    "Contemporary India – II",
    "Democratic Politics – II",
    "Understanding Economic Development"
  ],
  "English": [
    "First Flight - Prose and Poetry",
    "Footprints without Feet",
    "Grammar and Writing Skills"
  ]
};

document.addEventListener('DOMContentLoaded', () => {
  const subjectSelect = document.getElementById('subject');
  const chapterSelect = document.getElementById('chapter');

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
});
