

    document.addEventListener('DOMContentLoaded', function () {
      // Получаем ссылки на предыдущую и следующую страницы
      const prevButton = document.querySelector('.prev');
      const nextButton = document.querySelector('.next');
      
      // Получаем элемент для отображения текущей страницы
      const currentPageElement = document.querySelector('.current-page');
      
      // Начальная страница
      let currentPage = 1;
      
      // Обработчик для кнопки "Предыдущая"
      prevButton.addEventListener('click', function () {
        if (currentPage > 1) {
          currentPage--;
          updatePage();
        }
      });
      
      // Обработчик для кнопки "Следующая"
      nextButton.addEventListener('click', function () {
        const totalPages = 5;
        
        if (currentPage < totalPages) {
          currentPage++;
          updatePage();
        }
      });
      
      // Обновляем отображение текущей страницы
      function updatePage() {
        currentPageElement.textContent = currentPage;
      }
    });

