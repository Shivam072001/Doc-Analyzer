import {
  Component,
  Input,
  Output,
  EventEmitter,
  AfterViewInit,
  ViewChildren,
  ElementRef,
  OnDestroy,
  QueryList,
  OnInit,
} from '@angular/core';
import { fromEvent, Subscription, takeUntil, from } from 'rxjs'; // Import 'from'
import { Subject, merge } from 'rxjs';
import { ApiService } from '../../../../core/http/services/api.service';
import { DocumentService } from '../../../../shared/models/services/document.service';

interface SelectOption {
  label: string;
  value: string;
}

@Component({
  selector: 'app-pdf-query-section',
  standalone: false,
  templateUrl: './pdf-query-section.component.html',
  styleUrls: ['./pdf-query-section.component.scss'],
})
export class PdfQuerySectionComponent
  implements AfterViewInit, OnDestroy, OnInit
{
  @Input() promptTypes: string[] = [];
  @Input() query: string = '';
  @Input() response: string = '';
  @Input() chatHistoryStatus: string = '';
  @Input() isLoading: boolean = false;
  @Output() ask = new EventEmitter<void>();
  @Output() clearChat = new EventEmitter<void>();
  @Output() queryChange = new EventEmitter<string>();

  @ViewChildren('queryResponseContainer') responseContainers!: QueryList<
    ElementRef<HTMLDivElement>
  >;
  @ViewChildren('resizeHandle') resizeHandles!: QueryList<
    ElementRef<HTMLDivElement>
  >;

  private subscriptions: Subscription[] = [];
  private destroy$ = new Subject<void>();

  // New properties for document classification
  availableModels: SelectOption[] = [];
  selectedClassificationModel: string = '';
  documentTextToClassify: string = '';
  classificationResult: any;
  isClassifying: boolean = false;

  constructor(private readonly documentService: DocumentService) {}

  ngOnInit(): void {
    this.fetchAvailableModels();
  }

  fetchAvailableModels(): void {
    from(this.documentService.getAvailableModels<{ models: SelectOption[] }>())
      .pipe(takeUntil(this.destroy$))
      .subscribe(
        (data: { models: SelectOption[] }) => {
          this.availableModels = data.models;
          console.log('Available models:', this.availableModels);
        },
        (error: any) => {
          console.error('Error fetching available models:', error);
          // Handle error appropriately (e.g., display a message to the user)
        }
      );
  }

  onClassificationModelChange(modelValue: string): void {
    this.selectedClassificationModel = modelValue;
    console.log(
      'Selected classification model:',
      this.selectedClassificationModel
    );
    // Optionally, immediately set the model on the backend
    // this.setClassificationModelOnBackend(this.selectedClassificationModel);
  }

  setClassificationModelOnBackend(modelName: string): void {
    this.isClassifying = true;
    from(this.documentService.setModel(modelName))
      .pipe(takeUntil(this.destroy$))
      .subscribe(
        (response: any) => {
          console.log('Model set on backend:', response);
          this.classifyDocument();
        },
        (error: any) => {
          console.error('Error setting model on backend:', error);
          this.isClassifying = false;
          // Handle error
        }
      );
  }

  classifyDocument(): void {
    if (!this.selectedClassificationModel) {
      alert('Please select a document classification model.');
      return;
    }
    if (!this.documentTextToClassify) {
      alert('Please enter the document text to classify.');
      return;
    }

    this.isClassifying = true;
    from(
      this.documentService.classifyDocument(this.documentTextToClassify)
    )
      .pipe(takeUntil(this.destroy$))
      .subscribe(
        (response: any) => {
          console.log('Classification response:', response);
          this.classificationResult = response;
          this.isClassifying = false;
        },
        (error: any) => {
          console.error('Error classifying document:', error);
          this.classificationResult = { error: 'Could not classify document.' };
          this.isClassifying = false;
          // Handle error
        }
      );
  }

  ngAfterViewInit(): void {
    console.log('ngAfterViewInit called');
    console.log('resizeHandles:', this.resizeHandles);
    console.log('responseContainers:', this.responseContainers);

    this.resizeHandles.forEach((resizeHandleRef, index) => {
      const resizeHandle = resizeHandleRef.nativeElement;
      const responseContainer =
        this.responseContainers.toArray()[index]?.nativeElement;
      const responseElement = responseContainer?.querySelector(
        '.response'
      ) as HTMLElement;

      console.log('Processing handle at index:', index);
      console.log('resizeHandle element:', resizeHandle);
      console.log('responseContainer element:', responseContainer);
      console.log('responseElement:', responseElement);

      if (responseElement && resizeHandle) {
        let isResizing = false;
        let startY: number;
        let startHeight: number;

        const startResizing = (event: MouseEvent | TouchEvent) => {
          console.log('startResizing triggered', event);
          isResizing = true;
          startY =
            event instanceof TouchEvent
              ? event.touches[0].clientY
              : event.clientY;
          startHeight = parseInt(getComputedStyle(responseElement).height, 10);
          console.log('startY:', startY, 'startHeight:', startHeight);

          const mouseMove$ = fromEvent<MouseEvent | TouchEvent>(
            document,
            'mousemove'
          ).pipe(takeUntil(this.destroy$));
          const touchMove$ = fromEvent<TouchEvent>(document, 'touchmove').pipe(
            takeUntil(this.destroy$)
          );
          const mouseUp$ = fromEvent(document, 'mouseup').pipe(
            takeUntil(this.destroy$)
          );
          const touchEnd$ = fromEvent(document, 'touchend').pipe(
            takeUntil(this.destroy$)
          );

          const handleMove = (moveEvent: MouseEvent | TouchEvent) => {
            if (isResizing) {
              moveEvent.preventDefault();
              const clientY =
                moveEvent instanceof TouchEvent
                  ? moveEvent.touches[0].clientY
                  : moveEvent.clientY;
              let newHeight = startHeight + (clientY - startY);
              console.log(
                'clientY:',
                clientY,
                'newHeight before constraint:',
                newHeight
              );

              if (newHeight < 100) {
                newHeight = 100;
                console.log('New height after constraint:', newHeight);
              }
              responseElement.style.height = `${newHeight}px`;
            }
          };

          const stopResizing = () => {
            console.log('stopResizing triggered');
            isResizing = false;
            // ... (rest of stopResizing logic)
          };

          const moveSubscription = merge(mouseMove$, touchMove$).subscribe(
            handleMove
          );
          const endSubscription = merge(mouseUp$, touchEnd$).subscribe(
            stopResizing
          );
          this.subscriptions.push(moveSubscription, endSubscription);
        };

        const mousedownSubscription = fromEvent<MouseEvent>(
          resizeHandle,
          'mousedown'
        )
          .pipe(takeUntil(this.destroy$))
          .subscribe(startResizing);

        const touchstartSubscription = fromEvent<TouchEvent>(
          resizeHandle,
          'touchstart'
        )
          .pipe(takeUntil(this.destroy$))
          .subscribe(startResizing);

        this.subscriptions.push(mousedownSubscription, touchstartSubscription);
      }
    });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
    this.subscriptions.forEach((sub) => sub.unsubscribe());
  }

  onAsk(): void {
    this.ask.emit();
  }

  onClearChat(): void {
    this.clearChat.emit();
  }
}
