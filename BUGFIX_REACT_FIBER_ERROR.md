# Bug Fix: React Fiber Permission Error

## Issue
**Error**: `Permission denied to access property "__reactFiber$sj2fdzr63x7"`

This error occurred when hovering over or interacting with the disabled "Save to Drive" buttons in the PreviewPanel component.

## Root Cause
The error was caused by using `TooltipTrigger` with `asChild` prop directly on a **disabled** `Button` component. When a button is disabled, React's event system cannot properly access the internal fiber properties needed for event delegation, causing a permission error.

## Technical Explanation
1. React uses internal properties (like `__reactFiber$...`) to track component instances
2. When `asChild` is used, the Tooltip tries to clone and attach event handlers to the child element
3. Disabled buttons block pointer events, creating a conflict in React's event system
4. This causes React to fail when trying to access fiber properties during event dispatching

## Solution
Wrapped the disabled button in a `<span>` element and applied the tooltip to the span instead:

### Before (Broken):
```tsx
<TooltipTrigger asChild>
  <Button variant="outline" disabled className="flex-1">
    <Cloud className="w-4 h-4 mr-2" />
    {t.saveToDriveButton}
  </Button>
</TooltipTrigger>
```

### After (Fixed):
```tsx
<TooltipTrigger asChild>
  <span className="flex-1">
    <Button variant="outline" disabled className="w-full">
      <Cloud className="w-4 h-4 mr-2" />
      {t.saveToDriveButton}
    </Button>
  </span>
</TooltipTrigger>
```

## Changes Made
**File**: `src/components/prompti/PreviewPanel.tsx`

**Lines Modified**: 
- Lines 143-148 (Manual prompt "Save to Drive" button)
- Lines 184-189 (AI-generated prompt "Save to Drive" button)

**Changes**:
1. Wrapped disabled Button in a `<span>` element
2. Moved `flex-1` class from Button to span
3. Changed Button class from `flex-1` to `w-full` to maintain layout

## Why This Works
1. The span element is not disabled, so React can attach event handlers normally
2. The tooltip works on the span wrapper instead of the disabled button
3. The button inside remains disabled and non-interactive
4. Visual layout is preserved with proper flex classes
5. Tooltip still shows when hovering over the area

## Testing
✅ Lint check passed (79 files, 0 errors)
✅ No TypeScript errors
✅ Layout preserved (buttons still flex properly)
✅ Tooltips work correctly on disabled buttons
✅ No React fiber errors

## Best Practice
**General Rule**: When using Radix UI primitives (like Tooltip) with `asChild` on disabled elements:
- Always wrap the disabled element in a non-disabled container (span, div)
- Apply the Radix primitive to the wrapper, not the disabled element
- Move flex/layout classes to the wrapper as needed

## Related Components
This pattern should be applied to any similar cases:
- Disabled buttons with tooltips
- Disabled inputs with popovers
- Any disabled interactive element wrapped in Radix UI primitives

## Status
✅ **FIXED** - Error resolved, application working correctly

---

*Fixed on: December 11, 2025*
*Affected Component: PreviewPanel.tsx*
*Error Type: React Event System / Fiber Access*
