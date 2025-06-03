<template>
  <div class="calendar-wrap">
    <h4 class="mb-3">📅 독서 달력</h4>
    <v-calendar
      :attributes="calendarData"
      class="responsive-calendar"
      style="width: 100%; min-width: 0; max-width: 100%;"
    >
      <template #day-content="slotProps">
        <div>
          <span class="dayitem">{{ slotProps.day?.day }}</span>
          <div v-if="slotProps.attributes?.length">
            <div v-for="attr in slotProps.attributes" :key="attr.key">
              <div
                v-for="item in attr.customData?.content || []"
                :key="item.id"
                class="item"
              >
                <RouterLink :to="{ name: 'book-detail', params: { bookId: item.id } }" @click="console.log('📚 이동하는 bookId:', item.id)">
                  📖 {{ item.title }}
                </RouterLink>
              </div>
            </div>
          </div>
        </div>
      </template>
    </v-calendar>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import axios from 'axios'
import 'v-calendar/style.css'

const route = useRoute()
const accountStore = useAccountStore()
const username = route.params.username
const calendarData = ref([])

function truncateText(text, maxLength = 18) {
  if (text.length > maxLength) {
    return text.slice(0, maxLength) + '...'
  }
  return text
}

onMounted(async () => {
  try {
    const res = await axios.get(
      `http://127.0.0.1:8000/api/v1/users/${username}/calendar/`,
      {
        headers: {
          Authorization: `Token ${accountStore.token}`,
        }
      }
    )

    calendarData.value = res.data.map((item) => {
      let titleArr = Array.isArray(item.titles)
        ? item.titles
        : Object.values(item.titles || {})

      let idArr = Array.isArray(item.book_ids)
        ? item.book_ids
        : Object.values(item.book_ids || {})


      let contentArr = titleArr.map((title, index) => {
        const cleanTitle =
          typeof title === 'string'
            ? truncateText(title, 22)
            : (title && typeof title === 'object' && 'title' in title
                  ? truncateText(title.title, 22)
                  : truncateText(JSON.stringify(title), 22))

        return {
          title: cleanTitle,
          id: idArr[index] ?? -1
        }
      })

      return {
        key: item.date,
        dates: new Date(item.date),
        popover: {
          label: contentArr.length > 1
            ? contentArr.map(item => `- ${item.title}`).join('<br>')
            : `- ${contentArr[0]?.title || ''}`,
          visibility: 'hover'
        },
        customData: {
          content: contentArr
        }
      }
    })
  } catch (err) {
    console.error(err)
  }
})
</script>

<style>
.responsive-calendar {
  width: 100%;
}

.vc-weeks .vc-week {
  height: 100px;
}

.item {
  font-size: small;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  word-break: break-word;
}

.item a {
  color: inherit;
  text-decoration: none;
}

.item a:hover {
  text-decoration: underline;
}
</style>
