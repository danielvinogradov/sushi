const countNotifLimit = 3
const intervalTime = 300
const [toastrType, successStatus] = ["success", "success"]
let [notifToShow, showingNotif] = [new Map(), new Set()]
let buildedNotifInfo = new Map()
let notifData
const notIn = (setA, setB) => {
    let rSet = new Set()
    for(let key of setA) 
        if(!(setB.has(key))) 
            rSet.add(key)
    return rSet
}

const loadNotifications = (data, status, jqXHR) => {
    if (status != successStatus)
        return false 

    notifData = data
    
    let notifDataKeys = new Set()

    for(let key in notifData)
        notifDataKeys.add(key)

    if (notifDataKeys.size == 0)
        return false
    
    toBuild = notIn(notifDataKeys, new Set(buildedNotifInfo.keys()))
    console.log(buildedNotifInfo.size)
    for(let key of toBuild){
        buildedNotifInfo.set(key, buildNotificationInfo(notifData[key].type,
            notifData[key].status,
            notifData[key].entityId)) 
    }    
             
    let cnt = notifToShow.size                                                 
    for(let entityId of buildedNotifInfo){
        if (cnt == countNotifLimit)
            break
        ++cnt
        notifToShow.set(entityId, buildedNotifInfo.get(entityId))
    }

    return true
}

let eventStatusNew = 'new'
let eventStatyusUpdated = 'updated'

const buildNotificationInfo = (eventType, eventStatus, eventEntityId) => {
    let title, messege
    switch (eventType) {
        case 'task': 
            title = 'Задача ' + eventEntityId
            
            switch (eventStatus) {
                case eventStatusNew:
                    messege = 'Вам назначена новая задачa !'
                    break
                
                case eventStatyusUpdated:
                    messege = 'Изменение по задаче!'
                    break
            }

            break

        case 'feedback':
            title = 'Отзыв'

            switch (eventStatus) {
                case eventStatusNew:
                    messege = 'Новый отзыв!'
                    break

                case eventStatyusUpdated:
                    messege = 'Изменение по отзыву!'
                    break
            }

            break

        case 'messege':
            title = 'Сообщение'

            switch (eventStatus) {
                case eventStatusNew:
                    messege = 'Новое сообщение'
                    break

                case eventStatyusUpdated:
                    messege = 'Сообщение обновлено!'
                    break
            }

            break

        case 'idea':
            title = 'Идея'

            switch (eventStatus) {
                case 'accepted':
                    messege = 'Идея одобрена!'
                    break

                case 'rejected':
                    messege = 'Идея отклонена.'
                    break
            }

            break

        case 'shop':
            title = 'Магазин'

            switch (eventStatus) {
                case eventStatusNew:
                    messege = 'Создан новый магазин!'
                    break

                case eventStatyusUpdated:
                    messege = 'Изменение в магазине'
                    break
            }

            break

        
        case 'materials':
            title = 'Материалы'

            switch (eventStatus) {
                case eventStatusNew:
                    messege = 'Добавлены новые материалы'
                    break
            }

            break
    }
    return {'messege': messege, 'title': title } 
}

const onToastClose = (eventData) => {
    $.ajax({
        type: 'POST',
        url: baseUrl + 'notification-events',
        dataType: 'json',
        data: JSON.stringify(eventData.data.json_data),
        success: () => {
            //console.log(eventData.data.key)
            //showingNotif.delete(eventData.data.key)
            console.log('aaaaaaaaaaa')
        },
        error: function () {
            console.log('asdsad')
          },
    })
}

const showNotifications = () => {
    for(let [key, val] of buildedNotifInfo){
        if (showingNotif.has(key))
            continue

        let msg = val.messege
        let title = val.title
        let type = toastrType

        let myToast = toastr[type](msg, title, {
            positionClass: "toast-bottom-right",
            closeButton: true,
            progressBar: false,
            newestOnTop: true,
            timeOut : 0,
            tapToDismiss: false,
            extendedTimeOut: 0,
            rtl: $('body').attr('dir') === 'rtl' || $('html').attr('dir') === 'rtl'
        })
        
        evData = {
            'json_data': [key],
            'key': key
        }
        
        myToast.find('button').attr('entity-id', key)
                              .click(evData, onToastClose)
                    
        showingNotif.add(key)
    }
}

let baseUrl = new URL(document.URL).origin + '/'

const updateNotificationsEvent = () => {
    if (showingNotif.size < countNotifLimit){
        success = $.getJSON(baseUrl + 'load_notifications/', {}, loadNotifications)

        if (success) 
            showNotifications()
    }
}

setInterval(updateNotificationsEvent, intervalTime)